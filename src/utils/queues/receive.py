from kubemq.queue.message_queue import MessageQueue
if __name__ == "__main__":
    queue = MessageQueue("hello-world-queue", "test-queue-client-id2", "10.0.86.232:50000", 2, 1)
    try:
        res = queue.receive_queue_messages()
        if res.error:
            print(
                "'Received:'%s'" % (
                    res.error
                            )
            )
        else:
            for message in res.messages:
                print(
                        "'MessageID :%s ,Body: sending:'%s'" % (
                            message.MessageID,
                            message.Body
                                    )
                    )
    except Exception as err:
      print(
            "'error sending:'%s'" % (
                err
                        )
        )
    input("Press 'Enter' to stop the application...\n")