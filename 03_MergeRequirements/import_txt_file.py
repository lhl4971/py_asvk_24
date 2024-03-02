def import_txt_file(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            # Удаляем символы новой строки и лишние пробелы с конца строки
            clean_line = line.strip()
            # Проверяем, что строка содержит ровно 5 символов
            if len(clean_line) == 5:
                lines.append(clean_line)
            else:
                print(f"Ignoring line '{clean_line}' as it doesn't have exactly 5 characters.")
    return lines