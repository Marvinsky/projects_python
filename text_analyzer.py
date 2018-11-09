import unittest
import os

def analyze_text(filename):
    """Calculate the number of lines and characters in a file

    Args:
        filename: The name of the file to analyze.

    Raises:
        IOError: If 'filename' does not exists or can not be read

    Returns: A tuple where the first element is the number of lines
    and the second element is the number of chracteres
    """

    lines = 0
    chars = 0
    with open(filename, mode="r") as f:
        for line in f:
            lines += 1
            chars += len(line)
    return (lines, chars)


def text_number_lines(filename2):
    with open(filename2, mode="r") as f:
        return sum(1 for _ in f)


class TextAnalysisTests(unittest.TestCase):
    """Tests for the analyze_text() function"""
    def setUp(self):
        """Fixture that creates a file for the next method to use."""
        self.filename = "text_analysis_test_file.txt"
        with open(self.filename, mode="w") as f:
            f.write("Now we are engaged in a great civil war\n"
                    "testing whether that nation,\n"
                    "or any nation so conceived and so dedicated, \n"
                    "can log endure.")


        self.filename2 = "number_lines_file.txt"
        with open(self.filename2, mode="w") as f2:
            f2.write("Marvin Abisrror Zarate\n"
                     "Pooji Mariano Rodrigo\n"
                     "Goku vs Freezer"
                     )

    def tearDown(self):
        """Fixture that deletes the file used by the test methods."""
        try:
            os.remove(self.filename)
            os.remove(self.filename2)
        except:
            pass


    def test_function_runs(self):
        """Basic smocke test: does the function run."""
        analyze_text(self.filename)

    def test_line_count(self):
        a, b  = analyze_text(self.filename)
        self.assertEqual(a, 4)


    def test_function_run2(self):
        self.assertEqual(text_number_lines(self.filename2), 3)

    def test_characters_count(self):
        a, b = analyze_text(self.filename)
        self.assertEqual(b, 130)

    def test_no_such_file(self):
        """Check the proper exception is thrown for a missing file"""
        with self.assertRaises(IOError):
            analyze_text("foobar")


    def test_no_deletation(self):
        """Check that the function doesn't delete the input file."""
        analyze_text(self.filename)
        self.assertTrue(os.path.exists(self.filename))

if __name__ == "__main__":
    unittest.main()
