import tensorflow as tf

class MentionScorerModel():
    def __init__(self, hidden_size=512, lr=0.0005, keep_prob_input=0.5, keep_prob_dense=0.8, features_size=455):
        self.keep_prob_input = keep_prob_input
        self.keep_prob_dense = keep_prob_dense
        self.lr = lr

        self.A = tf.placeholder(dtype=tf.float32, shape=(None, features_size), name='A')
        self.B = tf.placeholder(dtype=tf.float32, shape=(None, features_size), name='B')

        self.A_features = tf.placeholder(dtype=tf.int32, shape=(None, 5), name='A_features')
        self.B_features = tf.placeholder(dtype=tf.int32, shape=(None, 5), name='B_features')

        self.AB_features = tf.placeholder(dtype=tf.int32, shape=(None, 2), name='AB_features')

        self.labels = tf.placeholder(dtype=tf.int32, shape=(None,), name='labels')
        self.keep_prob_input_ph = tf.placeholder(dtype=tf.float32, shape=(None), name='keep_prob_input_ph')
        self.keep_prob_dense_ph = tf.placeholder(dtype=tf.float32, shape=(None), name='keep_prob_dense_ph')
        self.roc_auc = tf.placeholder(dtype=tf.float32, shape=(None), name='roc_auc_ph')

        # TODO: get this from parameters?
        ohe_size = 10
        emb_dim = 10
        feat_2_embeddings = tf.Variable(tf.random_uniform([ohe_size, emb_dim], -1.0, 1.0, name='embeddings_2'), dtype=tf.float32)
        feat_3_embeddings = tf.Variable(tf.random_uniform([ohe_size, emb_dim], -1.0, 1.0, name='embeddings_3'), dtype=tf.float32)
        feat_4_embeddings = tf.Variable(tf.random_uniform([ohe_size, emb_dim], -1.0, 1.0, name='embeddings_4'), dtype=tf.float32)
        pair_0_embeddings = tf.Variable(tf.random_uniform([ohe_size, emb_dim], -1.0, 1.0, name='pair_0_embeddings'), dtype=tf.float32)
        pair_1_embeddings = tf.Variable(tf.random_uniform([ohe_size, emb_dim], -1.0, 1.0, name='pair_1_embeddings'), dtype=tf.float32)

        # we have to unstack them, because 2,3,4 features are not binary and would have learnable embdgs
        A_f_0, A_f_1, A_f_2, A_f_3, A_f_4 = tf.unstack(self.A_features, axis=1)
        B_f_0, B_f_1, B_f_2, B_f_3, B_f_4 = tf.unstack(self.B_features, axis=1)

        A_f_2_emb = tf.nn.dropout(tf.nn.embedding_lookup(feat_2_embeddings, A_f_2), keep_prob=self.keep_prob_input)
        A_f_3_emb = tf.nn.dropout(tf.nn.embedding_lookup(feat_3_embeddings, A_f_3), keep_prob=self.keep_prob_input)
        A_f_4_emb = tf.nn.dropout(tf.nn.embedding_lookup(feat_4_embeddings, A_f_4), keep_prob=self.keep_prob_input)
        B_f_2_emb = tf.nn.dropout(tf.nn.embedding_lookup(feat_2_embeddings, B_f_2), keep_prob=self.keep_prob_input)
        B_f_3_emb = tf.nn.dropout(tf.nn.embedding_lookup(feat_3_embeddings, B_f_3), keep_prob=self.keep_prob_input)
        B_f_4_emb = tf.nn.dropout(tf.nn.embedding_lookup(feat_4_embeddings, B_f_4), keep_prob=self.keep_prob_input)

        pair_0_f, pair_1_f = tf.unstack(self.AB_features, axis=1)
        pair_0_f_emb = tf.nn.dropout(tf.nn.embedding_lookup(pair_0_embeddings, pair_0_f), keep_prob=self.keep_prob_input)
        pair_1_f_emb = tf.nn.dropout(tf.nn.embedding_lookup(pair_1_embeddings, pair_1_f), keep_prob=self.keep_prob_input)

        A_f_emb = tf.concat([tf.cast(tf.expand_dims(A_f_0, axis=1), tf.float32), tf.cast(tf.expand_dims(A_f_1, axis=1), tf.float32),
                A_f_2_emb, A_f_3_emb, A_f_4_emb], axis=1, name='A_f_emb')
        B_f_emb = tf.concat([tf.cast(tf.expand_dims(B_f_0, axis=1), tf.float32), tf.cast(tf.expand_dims(B_f_1, axis=1), tf.float32),
                B_f_2_emb, B_f_3_emb, B_f_4_emb], axis=1, name='B_f_emb')

        A_do = tf.nn.dropout(self.A, keep_prob=self.keep_prob_input_ph)
        B_do = tf.nn.dropout(self.B, keep_prob=self.keep_prob_input_ph)
        A_encoded = tf.concat([A_do, A_f_emb], axis=1, name='A_encoded')
        B_encoded = tf.concat([B_do, B_f_emb], axis=1, name='B_encoded')
        inputs = tf.concat([A_encoded, B_encoded, A_encoded * B_encoded, pair_0_f_emb, pair_1_f_emb], axis=1)

        dense_1 = tf.layers.dense(inputs, units=hidden_size, activation=tf.nn.tanh, kernel_initializer=tf.contrib.layers.xavier_initializer())
        dense_1_do = tf.nn.dropout(dense_1, keep_prob=self.keep_prob_dense_ph)
        dense_2 = tf.layers.dense(dense_1_do, units=hidden_size//2, activation=tf.nn.tanh, kernel_initializer=tf.contrib.layers.xavier_initializer())
        dense_2_do = tf.nn.dropout(dense_2, keep_prob=self.keep_prob_dense_ph)
        self.logits = tf.layers.dense(dense_2_do, units=2, kernel_initializer=tf.contrib.layers.xavier_initializer())
        self.pred = tf.nn.softmax(self.logits)

        lables_ohe = tf.one_hot(self.labels, depth=2)
        cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=lables_ohe, logits=self.logits)
        self.loss = tf.reduce_mean(cross_entropy)
        self.loss_summary = tf.summary.scalar("loss", self.loss)
        self.loss_test_summary = tf.summary.scalar("loss_test", self.loss)
        self.roc_auc_summary = tf.summary.scalar("roc_auc", self.roc_auc)
        
        self.train_op = tf.contrib.layers.optimize_loss(loss=self.loss, global_step=tf.contrib.framework.get_global_step(),
            learning_rate=self.lr, optimizer='Adam')

    def train_batch(self, session, A, A_f, B, B_f, AB_f, labels):
        feed_dict = {
            self.A: A,
            self.A_features: A_f,
            self.B: B,
            self.B_features: B_f,
            self.AB_features: AB_f,
            self.labels: labels,
            self.keep_prob_input_ph: self.keep_prob_input,
            self.keep_prob_dense_ph: self.keep_prob_dense,
        }
        loss, loss_sum, logits, _ = session.run(
            [self.loss, self.loss_summary, self.logits, self.train_op],
            feed_dict=feed_dict)
        return loss, loss_sum, logits

    def test_batch(self, session, A, A_f, B, B_f, AB_f, labels):
        feed_dict = {
            self.A: A,
            self.A_features: A_f,
            self.B: B,
            self.B_features: B_f,
            self.AB_features: AB_f,
            self.labels: labels,
            self.keep_prob_input_ph: 1.0,
            self.keep_prob_dense_ph: 1.0,
        }
        loss, loss_sum, logits, pred = session.run([self.loss, self.loss_test_summary, self.logits, self.pred],
            feed_dict=feed_dict)

        return loss, loss_sum, logits, pred