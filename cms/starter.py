from datetime import date
import os


# Default location
MARKDOWN_DIR = './markdown'

def generate_date_string():
    """Get date string in the form of MonthName Day, Year"""
    today = date.today() 

    months = {
        1: 'January',
        2: 'Febuary',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    month = months[today.month]
    day = today.day
    year = today.year

    return '{0} {1}, {2}'.format(month, day, year)


def generate_starter():
    """Generate a starter markdown file"""

    metadata = [
        input('Enter title: ').strip(),
        input('Enter author: ').strip(),
        generate_date_string(),
        input('Enter image: ').strip(),
        input('Enter blurb: ').strip(),
        input('Enter permalink: '.strip())
    ]

    assert metadata[-1], 'Must provide a non-empty permalink'

    preamble = '\n'.join([
        'title: ' + metadata[0],
        'author: ' + metadata[1],
        'date: ' + metadata[2],
        'image: ' + metadata[3],
        'blurb: ' + metadata[4],
        'permalink: ' + metadata[5]
    ]) + '\n'

    filename = '{name}.md'.format(name=metadata[-1])
    location = os.path.join(MARKDOWN_DIR, filename)

    i = 1
    while os.path.isfile(location):
        # Rename if the file already exists
        filename = '{name}-{id}.md'.format(name=metadata[-1], id=i)
        location = os.path.join(MARKDOWN_DIR, filename)
        i += 1

    with open(location, 'w') as f:
        f.write(preamble)


if __name__ == '__main__':
    generate_starter()