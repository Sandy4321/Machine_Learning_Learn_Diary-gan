# coding=utf-8
import tensorflow as tf
import pylab as plt

flags = tf.flags.FLAGS

# tf.flags.DEFINE_string('buckets', './', "输入目录")
# tf.flags.DEFINE_string('stdoutDir', './', '输出目录')


tf.flags.DEFINE_string('buckets', 'oss://mlearn.oss-cn-shanghai-internal.aliyuncs.com/classify/', "输入目录")
tf.flags.DEFINE_string('stdoutDir', 'oss://mlearn.oss-cn-shanghai-internal.aliyuncs.com/classify_resize/stdout/', '输出目录')


def main(args=None):
    files = tf.gfile.Glob(flags.buckets + "*.jpg")
    file_queue = tf.train.input_producer(files)
    reader = tf.WholeFileReader()
    filename, image = reader.read(file_queue)
    image = tf.image.decode_jpeg(image, 3)
    image = tf.image.resize_images(image, [256, 256])
    image = tf.cast(image, tf.uint8)
    sess = tf.InteractiveSession()
    tf.train.start_queue_runners(sess=sess)
    sess.run(tf.global_variables_initializer())
    for step in xrange(len(files)):
        name_read, image_read = sess.run([filename, image])
        plt.imshow(image_read)
        plt.imsave(flags.stdoutDir + name_read, image_read)
        print step

if __name__ == "__main__":
    tf.app.run()
