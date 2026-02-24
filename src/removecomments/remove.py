
# ##############################################################################
# Imports
# ##############################################################################

# General
import copy
import numpy as np

# ##############################################################################
# Functions
# ##############################################################################


# ------------------------------------------------------------------------------
# Get Functions
# ------------------------------------------------------------------------------


def get_lines(file: str) -> list:
    """
        Gets the list with the lines.

        :param file: The full path to the file to be opened.

        :return: The list with the lines.
    """

    # Open and read the lines.
    with open(file, mode="r", newline="\n") as file:
        lines = list(file.readlines())

    # Strip from leading white spaces.
    for i, line in enumerate(lines):
        lines[i] = line.rstrip().lstrip("\n")

    return lines


def get_new_line(incomment: bool, line: str, linenumber: int) -> tuple:
    """
        Gets the list with the new lines to append to the new line.

        :param incomment: .

        :param line: The line that is being stripped off the comments.

        :param linenumber: The number of the line in the file being checked.

        :return: The list with the lines and the index at which the next check
         must start.
    """

    # ##########################################################################
    # Auxiliary Functions
    # ##########################################################################

    def get_mlcmmnt(tline: str) -> tuple:
        """
            Gets the multiline comment, if needed.

            :param tline: The line from where the string will get extracted.

            :return: The tuple with the string to attach and the remaining
             string.
        """

        # Get the next character.
        for i, _ in enumerate(tline):
            # When the character is found.
            if tline[i: i + 2] == "*/":
                return False, tline[i + 2:]

        return True, ""

    def get_strchar(tline: str, tchars: str) -> tuple:
        """
            Gets the string up to the end of the given character.

            :param tline: The line from where the string will get extracted.

            :param tchars: The character/string that the algorithm must find
             before exiting.

            :return: The tuple with the string to attach and the remaining
             string.
        """

        # Get the next character.
        for i, tchar in enumerate(tline):
            # When the character is found.
            if tchars == tchar:
                if i > 0 and tline[i - 1] == "\\":
                    continue
                return tline[:i + 1], tline[i + 1:]

    def first_occurrence(tline: str, strng: str) -> int:
        """
            Returns the first occurrence of the given string.

            :param tline: The line that contains the string.

            :param strng: The string whose first occurrence if to be found.

            :param location: The location of the index where the string was
             passed.

            :return: The index with the first ocurrence of the string.
        """

        # The character.
        for i, char in enumerate(tline):
            # Retrieve the character to be analized.
            char = tline[i: i + len(strng)]

            # If the string is found.
            if char == strng:
                return i

        return np.inf

    # ##########################################################################
    # Implementations
    # ##########################################################################

    # Auxiliary variables.
    nline = ""
    vline = copy.deepcopy(line)
    keys = ["'", '"', "/*", "//"]

    # Search if in comments.
    if incomment:
        # Seek if still in comment.
        incomment, vline = get_mlcmmnt(line)

    while not incomment and len(vline) > 0:
        # Get the first occurrence of a character, or a string, etc.
        index = list(first_occurrence(vline, x) for x in keys)
        order = np.argsort(index)

        # All indexes are out of bounds.
        if index[order[0]] == np.inf:
            nline += vline
            return incomment, nline

        # Get the character of first occurrence.
        first = keys[order[0]]
        index = index[order[0]]

        # Get the string or character.
        if first == "'" or first == '"':
            nline += vline[:index + 1]
            tmp, vline = get_strchar(vline[index + 1:], vline[index])
            nline += tmp
            continue

        # String is finalized.
        if first == "/*":
            nline += vline[:index]
            incomment, vline = get_mlcmmnt(vline[index + 2:])
            continue

        # String is finalized.
        if first == "//":
            nline += vline[:index]
            return incomment, nline

    # Remove the comments.
    return incomment, nline


# ------------------------------------------------------------------------------
# Remove Functions
# ------------------------------------------------------------------------------


def remove_comments(lines: list) -> list:
    """
        Removes the comments from the file.

        :param lines: The lines of the c code.

        :return: The new list with the comments removed.
    """

    # The new list.
    nlines = list()
    incomment = False

    # Remove the comments.
    for i, line in enumerate(lines):
        incomment, line = get_new_line(incomment, line, i)
        nlines.append(line)

    return nlines


# ##############################################################################
# Main Function
# ##############################################################################


def main() -> None:
    """
        Run the main program.
    """
    file = "test.c"
    lines = get_lines(file)
    lines = remove_comments(lines)


# ##############################################################################
# Main Program
# ##############################################################################


if __name__ == "__main__":
    main()
