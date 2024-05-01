import logging
import sys

from wqet_grader.utils import set_grading_content_path

if len(sys.argv) < 2:
    set_grading_content_path("./course-assessment/")
else:
    set_grading_content_path(sys.argv[1])

from wqet_grader.server import app  # noQA E402

app.logger.setLevel(logging.DEBUG)
app.run(host="localhost", port=2400, debug=True, threaded=False)
