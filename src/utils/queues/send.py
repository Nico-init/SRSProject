from kubemq.queue.message_queue import MessageQueue

from kubemq.queue.message import Message


if __name__ == "__main__":

    queue = MessageQueue("hello-world-queue", "test-queue-client-id2", "10.0.86.232:50000")
    message = Message()
    message.metadata = 'metadata'
    message.body = "some-simple_queue-queue-message".encode('UTF-8')
    message.attributes = None
    try:
        sent  = queue.send_queue_message(message)
        if sent.error:
            print('message enqueue error, error:' + sent.error)
        else:
            print('message sent at: %d' % (
                sent.sent_at
                        ))
    except Exception as err:
        print('message enqueue error, error:%s'  % (
                err
                        ))