import os
from test.testlib import *
from git_python import Git
from git_python import errors

class TestGit(object):
    def setup(self):
        base = os.path.join(os.path.dirname(__file__), "../..")
        self.git = Git(base)

    @patch(Git, 'execute')
    def test_method_missing_calls_execute(self, git):
        git.return_value = ''
        self.git.version()
        assert_true(git.called)
        # assert_equal(git.call_args, ((("%s version " % self.git_bin_base),), {}))
    
    def test_it_transforms_kwargs_into_git_command_arguments(self):
        assert_equal(["-s"], self.git.transform_kwargs(**{'s': True}))
        assert_equal(["-s5"], self.git.transform_kwargs(**{'s': 5}))

        assert_equal(["--max-count"], self.git.transform_kwargs(**{'max_count': True}))
        assert_equal(["--max-count=5"], self.git.transform_kwargs(**{'max_count': 5}))
        
        assert_equal(["-s", "-t"], self.git.transform_kwargs(**{'s': True, 't': True}))

    def test_it_executes_git_to_shell_and_returns_result(self):
        assert_match('^git version [\d\.]*$', self.git.execute(["git","version"]))

    def test_it_accepts_stdin(self):
        filename = fixture_path("cat_file_blob")
        fh = open(filename, 'r')
        assert_equal( "70c379b63ffa0795fdbfbc128e5a2818397b7ef8",
                      self.git.hash_object(istream=fh, stdin=True) )
        fh.close()

    def test_it_returns_status_and_ignores_stderr(self):
        assert_equal( (1, ""), self.git.this_does_not_exist(with_status=True) )

    def test_it_raises_errors(self):
        error_raised = False
        try:
            self.git.this_does_not_exist(with_exceptions=True)
        except errors.GitCommandError, e:
            error_raised = True
        assert_equal( True, error_raised )
