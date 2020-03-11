import re

from foundations_spec import Spec, set_up, tear_down
from foundations_contrib.utils import run_command, cd, wait_for_condition


class TestTensorboardServer(Spec):
    @set_up
    def set_up(self):
        run_command(f"docker-compose up -d --force-recreate tb_server")
        run_command(f"docker-compose logs -f > .foundations/logs/tb_server.log 2>&1 &")
        wait_for_condition(self.tb_server_is_ready, timeout=5)

    @staticmethod
    def tb_server_is_ready():
        try:
            run_command("curl localhost:6006", quiet=True)
        except:
            return False
        else:
            return True

    @tear_down
    def tear_down(self):
        run_command("docker-compose stop tb_server")
        run_command("docker-compose rm -f tb_server")

    def test_starts_tensorboard_server(self):
        container_logs = run_command("docker-compose logs tb_server").stdout.decode()
        expected_message = re.compile(
            r"TensorBoard [0-9.]+ at http:\/\/[0-9a-f]{12}:6006\/ \(Press CTRL\+C to quit\)"
        )
        try:
            self.assertIsNotNone(expected_message.search(container_logs))
        except AssertionError:
            msg = "\n".join(
                [
                    f"Expected regex {expected_message.pattern} was not found in the container logs.",
                    "Container logs:",
                    container_logs,
                ]
            )
            self.fail(msg)
