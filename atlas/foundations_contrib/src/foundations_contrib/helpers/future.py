

class Future(object):

    @staticmethod
    def all(futures):
        from promise import Promise

        promises = [future._promise for future in futures]
        promise = Promise.all(promises)
        return Future(promise)
    
    @staticmethod
    def execute(target, *args, **kwargs):
        from foundations_contrib.global_state import default_executor
        from promise import Promise

        def callback(resolve, reject):
            def _internal():
                try:
                    resolve(target(*args, **kwargs))
                except Exception as error:
                    reject(error)
            return default_executor.submit(_internal)

        promise = Promise(callback)
        return Future(promise)

    def __init__(self, promise):
        self._promise = promise

    def get(self):
        return self._promise.get()