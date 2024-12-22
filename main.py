import os
import json

#checks to see if the file exists
def check_file_exists(filename):
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        exit()

# checks to see if the file has proper JSON data
def read_json_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print(f"Error: The file '{filename}' contains invalid JSON.")
            exit()

def check_key_exists(data, key_path):
    keys = key_path.split('.')
    current_data = data
    for key in keys:
        if not isinstance(current_data, dict) or key not in current_data:
            print(f"Error: Key '{key_path}' not found in JSON data.")
            exit()
        current_data = current_data[key]
    return current_data

# writes the new JSON data to the JSON file
def write_json_to_file(data, output_filename):
    with open(output_filename, "w") as outfile:
        analyze_result = check_key_exists(data, "analyzeResult")
        documents = check_key_exists(analyze_result, "documents")

        if isinstance(documents, list):
            for document in documents:
                fields = check_key_exists(document, "fields")
                po = check_key_exists(fields, "PurchaseOrder")
                date = check_key_exists(fields, "InvoiceDate")
                address = check_key_exists(fields, "VendorAddress")
                vendor_content = check_key_exists(address, "content").replace('\n', ' ')
                name = check_key_exists(fields, "VendorName")

                outfile.write('{\n')
                outfile.write(f'\t"purchase_order": "{check_key_exists(po, "content")}",\n')
                outfile.write(f'\t"invoice_date": "{check_key_exists(date, "content")}",\n')
                outfile.write(f'\t"vendor_address": "{vendor_content}",\n')
                outfile.write(f'\t"vendor_name": "{check_key_exists(name, "content")}",\n')

                outfile.write('\t"order_line_items": [\n')

                items = check_key_exists(fields, "Items")
                values = check_key_exists(items, "valueArray")
                if isinstance(values, list):
                    for value in values:
                        object = check_key_exists(value, "valueObject")
                        outfile.write("\t\t{\n")

                        code = check_key_exists(object, "ProductCode")
                        outfile.write(f'\t\t\t"product_code": "{check_key_exists(code, "content")}",\n')

                        description = check_key_exists(object, "Description")
                        description_content = check_key_exists(description, "content").replace('\n', ' ')
                        outfile.write(f'\t\t\t"description": "{description_content}",\n')

                        qty = check_key_exists(object, "Quantity")
                        outfile.write(f'\t\t\t"qty": "{check_key_exists(qty, "content")}",\n')

                        price = check_key_exists(object, "UnitPrice")
                        outfile.write(f'\t\t\t"price": "{check_key_exists(price, "content")}",\n')

                        amount = check_key_exists(object, "Amount")
                        outfile.write(f'\t\t\t"amount": "{check_key_exists(amount, "content")}"\n')

                        if value is values[-1]:
                            outfile.write("\t\t}\n")  # No comma for the last item
                        else:
                            outfile.write("\t\t},\n")

                    outfile.write("\t]\n")
                    outfile.write('}\n')

def main():
    num = int(input("How many files do you want to convert? "))
    for x in range(num):
        filename = input("What is the filename? ")
        output_filename = input("What is the output filename? ")

        check_file_exists(filename)
        json_data = read_json_file(filename)
        write_json_to_file(json_data, output_filename)

if __name__ == "__main__":
    main()
