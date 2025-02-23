import json
import random
import re

def read_file(file_path):
    """Đọc dữ liệu từ file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def parse_product_data(product_lines):
    """Phân tích dữ liệu sản phẩm từ file txt, trích xuất thông số kỹ thuật chi tiết"""
    products = []
    product = {}
    detailed_specs = {}

    spec_patterns = {
    "Công nghệ CPU": r"Công nghệ CPU::\s*([^|,]+)",
    "RAM": r"RAM::\s*([^|,]+)",
    "Ổ cứng": r"Ổ cứng::\s*([^|,]+)",
    "Màn hình": r"Màn hình::\s*([\d.]+\")",
    "Card màn hình": r"Card màn hình::\s*([^|,]+)",
    "Thông tin Pin": r"Thông tin Pin::\s*([^|,]+)",
}



    for line in product_lines:
        if line.startswith("ID:"):
            if product:
                product["Thông số chi tiết"] = detailed_specs
                products.append(product)
            product = {"ID": line.split(": ", 1)[1]}
            detailed_specs = {"CPU": "Không có thông tin", "RAM": "Không có thông tin", "Ổ cứng": "Không có thông tin", "Màn hình": "Không có thông tin"}
        elif line.startswith("Thông số chi tiết:"):
            continue
        elif ": " in line:
            key, value = line.split(": ", 1)
            key, value = key.strip(), value.strip()
            # print(f"Debug - Key: {key}, Value: {value}")

            matched = False
            for spec_category, pattern in spec_patterns.items():
                match = re.search(pattern, value)
                if match:
                    print(f"Matched {spec_category}: {match.group(1)}")
                    detailed_specs[spec_category] = match.group(1).replace(", ", "").strip()
                    matched = True

            
            if not matched:
                product[key] = value

    if product:
        product["Thông số chi tiết"] = detailed_specs
        products.append(product)

    return products

def extract_keywords(text):
    """Phân loại từ khóa từ câu hỏi"""
    words = text.lower().split()
    stopwords = {"là", "có", "bao", "nhiêu", "giá", "gì", "sao", "không", "của", "với", "cho"}
    
    # Nhóm từ khóa quan trọng
    product_keywords = set()
    attribute_keywords = set()
    action_keywords = set()
    
    attribute_patterns = {
        "cấu hình": r"\b(cấu hình|thông số|chi tiết|specs?)\b",
        "màn hình": r"\b(màn hình|inch|độ phân giải)\b",
        "CPU": r"\b(cpu|vi xử lý|chip)\b",
        "RAM": r"\b(ram|bộ nhớ ram)\b",
        "SSD": r"\b(ssd|ổ cứng|dung lượng)\b",
        "giá": r"\b(giá|bao nhiêu|đắt|rẻ)\b"
    }
    
    for word in words:
        if word in stopwords:
            continue
        matched = False
        for key, pattern in attribute_patterns.items():
            if re.search(pattern, word):
                attribute_keywords.add(key)
                matched = True
                break
        if not matched:
            product_keywords.add(word)

    return product_keywords, attribute_keywords, action_keywords

def find_relevant_products(question, products):
    """Tìm sản phẩm phù hợp dựa trên từ khóa"""
    product_keywords, attribute_keywords, _ = extract_keywords(question)
    
    matched_products = []
    for product in products:
        name_keywords = set(product.get("Tên", "").lower().split())
        specs_keywords = set(product.get("Thông số", "").lower().split())

        if product_keywords & name_keywords or product_keywords & specs_keywords:
            matched_products.append(product)

    return matched_products

def generate_responses(question, products):
    """Tạo câu trả lời phù hợp với câu hỏi với nhiều cách diễn đạt khác nhau"""
    relevant_products = find_relevant_products(question, products)
    
    if not relevant_products:
        relevant_products = random.sample(products, min(len(products), 3))
    
    product_keywords, attribute_keywords, _ = extract_keywords(question)
    response_list = []
    
    response_templates = [
        "Dạ có shop tôi có sản phẩm {name} với giá {price}.",
        "Chúng tôi xin giới thiệu {name} có giá {price}.",
        "Vâng sản phẩm {name} hoàn toàn phù hợp với yêu cầu của bạn!",
        "Tôi thấy {name} là một lựa chọn hợp lý, giá chỉ {price}.",
        "Bên shop tôi có {name}, bạn có thể tham khảo với mức giá {price}.",
        "Shop xin tư vấn cho bạn sản phẩm {name}, hiện tại sản phẩm chỉ có giá là {price}.",
        "{name} là một sản phẩm tốt, hiện đang có giá {price}.",
        "Bạn có thể xem qua {name}, giá chỉ {price} và rất phù hợp với tài chính hiện tại của bạn."
    ]

    spec_templates = [
        "{name} có {cpu}, {ram}, {storage}, màn hình {screen}. Hiện tại có giá {price}.",
        "Nếu bạn cần một sản phẩm mạnh mẽ, {name} với {cpu}, RAM {ram}, và {storage} sẽ đáp ứng nhu cầu. Giá bán: {price}.",
        "Cấu hình của {name}: {cpu}, {ram}, {storage}, màn hình {screen}. Giá hiện tại là {price}.",
        "{name} sử dụng {cpu}, kết hợp với {ram} và {storage}, màn hình {screen}, đảm bảo hiệu suất tốt. Giá: {price}.",
        "Với {name}, bạn sẽ có {cpu}, {ram}, {storage}",
        "Thông số kỹ thuật của {name}: {cpu}, {ram}, {storage}",
        "Sản phẩm {name} sử dụng {cpu}, {ram}, {storage}, dung lượng pin lên tới {battery}. Giá: chỉ {price}.",
        "Con laptop {name} này sử dụng {cpu}, {ram}, {storage}. Với card đồ họa {card_screen} mạnh mẽ. Giá: {price}. Phù hợp với kinh tế của bạn."
    ]

    for product in relevant_products:
        name = product.get('Tên', 'Sản phẩm không rõ')
        price = product.get('Giá', 'không xác định')
        
        specs = product.get("Thông số chi tiết", {})
        cpu = specs.get("Công nghệ CPU", "Không có thông tin CPU")
        ram = specs.get("RAM", "Không có thông tin RAM")
        storage = specs.get("Ổ cứng", "Không có thông tin ổ cứng")
        screen = specs.get("Màn hình", "Không có thông tin màn hình")
        battery = specs.get("Thông tin Pin", "Không có thông tin Pin")
        card_screen = specs.get("Card màn hình", "Không có thông tin Card màn hình")



        if attribute_keywords:
            template = random.choice(spec_templates)
            response = template.format(name=name, price=price, cpu=cpu, ram=ram, storage=storage, screen=screen, battery=battery, card_screen=card_screen)
        else:
            template = random.choice(response_templates)
            response = template.format(name=name, price=price)
        
        if response not in response_list:
            response_list.append(response)

    return response_list



def generate_qa_data(questions, products):
    """Tạo dữ liệu Q&A từ danh sách câu hỏi và sản phẩm"""
    qa_data = []
    for question in questions:
        responses = generate_responses(question, products)
        qa_data.append({
            "question": question,
            "answers": responses
        })
    return qa_data

def main():
    questions = read_file("./src/data/txt/question_data.txt")
    product_lines = read_file("./src/data/txt/product_data.txt")
    products = parse_product_data(product_lines)

    # # Kiểm tra dữ liệu sản phẩm đã được phân tích
    # for product in products:
    #     print(f"ID: {product.get('ID', 'Không có ID')}")
    #     print(f"Tên: {product.get('Tên', 'Không có tên')}")
    #     print(f"Giá: {product.get('Giá', 'Không có giá')}")
        
    #     specs = product.get("Thông số chi tiết", {})
    #     print(f"CPU: {specs.get('Công nghệ CPU', ['Không có thông tin CPU'])}")
    #     print(f"RAM: {specs.get('RAM', ['Không có thông tin RAM'])}")
    #     print(f"Ổ cứng: {specs.get('Ổ cứng', ['Không có thông tin ổ cứng'])}")
    #     print(f"Card màn hình: {specs.get('Card màn hình', ['Không có thông tin Card màn hình'])}")
    #     print(f"Thông tin Pin: {specs.get('Thông tin Pin', ['Không có thông tin Thông tin Pin'])}")
        
    #     print("="*50)

    # Tiếp tục xử lý dữ liệu Q&A
    qa_data = generate_qa_data(questions, products)
    
    with open("./src/data/json/dataset.json", "w", encoding="utf-8") as json_file:
        json.dump(qa_data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()

