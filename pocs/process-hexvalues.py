import magic, mimetypes


print('Processing data...')
with open('input.txt') as infile:
    for line in infile:
        line_values = line.split()
        try:
            if(len(line_values) > 0):
                file_name = line_values[0]
                print(f'Writting {file_name} files...')
                for file_id,value in enumerate(line_values[1:]):
                    file = bytes.fromhex(value.replace('0x',''))
                    file_ext = magic.from_buffer(file).split()[0].lower()

                    with open(f'{file_name}-{file_id}.{file_ext}', "wb") as outfile:
                        outfile.write(file)
        except:
            pass
