# -*- coding: utf-8 -*-
import  tensorflow as tf
import  input_data
#define get_data
mnist=input_data.read_data_sets("./MNIST_data",one_hot=True)

#params
train_rate=0.001
train_step=1000
batch_size=1280
display_step=100

frame_size=28
sequence_length=28
hidden_num=100
# =============================================================================
# hiden num is the dimention of the hidden layer,not the num of hidden cells.general 
# every inout[batch,seq_length,depth] will have a output[batch,seq_length,hidden_num],
# you can get the final output:output[:,-1,:]=>[batch,hidden_num]
# in this exampple,then you can changed the dimention to class num by w*final_output
# =============================================================================
n_classes=10

#定义输入,输出
x=tf.placeholder(dtype=tf.float32,shape=[None,sequence_length*frame_size],name="inputx")
y=tf.placeholder(dtype=tf.float32,shape=[None,n_classes],name="expected_y")
#定义权值
weights=tf.Variable(tf.truncated_normal(shape=[hidden_num,n_classes]))
bias=tf.Variable(tf.zeros(shape=[n_classes]))

def RNN(x,weights,bias):
    x=tf.reshape(x,shape=[-1,sequence_length,frame_size])
    rnn_cell=tf.nn.rnn_cell.BasicRNNCell(hidden_num)
    #initial_state = rnn_cell.zero_state(batch_size, dtype=tf.float32)
    #init_state=tf.zeros(shape=[batch_size,rnn_cell.state_size])
    #init_state=rnn_cell.zero_state(batch_size, dtype=tf.float32)
    # 其实这是一个深度RNN网络,对于每一个长度为n的序列[x1,x2,x3,...,xn]的每一个xi,都会在深度方向跑一遍RNN,跑上hidden_num个隐层单元
    #output,states=tf.nn.dynamic_rnn(rnn_cell,x,initial_state=init_state,dtype=tf.float32)
    output,states=tf.nn.dynamic_rnn(rnn_cell,x,dtype=tf.float32)
    return tf.nn.softmax(tf.matmul(output[:,-1,:],weights)+bias,1)
predy=RNN(x,weights,bias)
cost=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=predy,labels=y))
train=tf.train.AdamOptimizer(train_rate).minimize(cost)

correct_pred=tf.equal(tf.argmax(predy,1),tf.argmax(y,1))
accuracy=tf.reduce_mean(tf.to_float(correct_pred))


config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)
sess.run(tf.initialize_all_variables())
step=1
testx,testy=mnist.test.next_batch(batch_size)
while step<train_step:
    batch_x,batch_y=mnist.train.next_batch(batch_size)
#    batch_x=tf.reshape(batch_x,shape=[batch_size,sequence_length,frame_size])
    _loss,__=sess.run([cost,train],feed_dict={x:batch_x,y:batch_y})
    if step % display_step ==0:
        acc,loss=sess.run([accuracy,cost],feed_dict={x:testx,y:testy})
        print(step,acc,loss)
    step+=1

