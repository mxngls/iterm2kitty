import os
import sys
import plistlib


def close(s):
    print(s)
    sys.exit(1)


# Convert colors from RGB to Hex
def convert_to_buf(key_pair, iterm_obj, buf):
    palette = ['Red', 'Green', 'Blue']

    if key_pair[0] not in iterm_obj:
        cloz("Missing key: %s\n check file" % key_pair[0])
    color_dict = iterm_obj[key_pair[0]]
    hex_color = "#"
    for color in palette:
        color_key = "%s Component" % color
        if color_key not in color_dict:
            close("Missing RGB key: %s\n Check the iterm colorscheme" %
                  color_key)
        color_hex = hex(int(round(color_dict[color_key] * 255))).split('x')[1]

        if len(color_hex) < 2:
            color_hex = '0' + color_hex
        hex_color += color_hex.lower()
    buf += "%s %s\n" % (key_pair[1], hex_color)
    return buf


def main():
    for file in sys.argv[1:]:
        print("File: %s" % file)
        with open(file, 'rb') as f:
            iterm_obj = plistlib.load(f)
            buf = ''

            # Plain Ansi Colors
            for i in range(16):
                key_pair = ("Ansi %d Color" % i, "color%d" % i)
                buf = convert_to_buf(key_pair, iterm_obj, buf)

            # Special fields (cursor, foreground, background etc)
            # See https://raw.githubusercontent.com/kovidgoyal/kitty-themes/master/template.conf
            # for a list of all available fields
            cursor = ("Cursor Color", "cursor")
            cursor_text = ("Cursor Text Color", "cursor_text_color")
            foreground = ("Foreground Color", "foregroubd")
            background = ("Background Color", "background")
            selection_text = ("Selected Text Color", "selection_foreground")
            selection = ("Selected Text Color", "selection_background")
            url_color = ("Link Color", "url_color")

            special = [
                cursor, cursor_text, foreground, background, selection_text
            ]

            for key_pair in special:
                buf = convert_to_buf(key_pair, iterm_obj, buf)

            output_file_name = os.path.basename(file).replace(' ',
                                                              '_') + '.conf'
            with open(output_file_name, 'w') as outfile:
                outfile.write(buf)
            print("The outfile is: %s" % output_file_name)


if __name__ == "__main__":
    main()
