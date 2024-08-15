from contextlib import contextmanager
import traceback
from logging import Logger

class BaseService:
    _logger: Logger

    @contextmanager
    def handle_exception(self):
        try:
            yield
        except Exception as e:
            traceback.print_exc()
            self._logger.error(str(e))