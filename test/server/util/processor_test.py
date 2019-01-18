from asciiarena.server.util.processor import Processor, Request, Reply, ProcessingError

class MyProcessor(Processor):
    def __init__(self):
        Processor.__init__(self)
        pass

    def process_request(self, request):
        return Reply([request.sender], request.message)

def test_put_request_get_reply():
    processor = MyProcessor()
    processor.run()

    request = Request(1, "message")
    processor.enqueue_request(request)
    reply = processor.dequeue_reply()

    processor.stop()

    assert request.message == reply.message
    assert request.sender == reply.receiver_list[0]

