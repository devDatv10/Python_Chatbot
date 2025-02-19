import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

with open("./src/data/txt/product_data.txt", "w", encoding="utf-8") as f:
    page = 1 

    while True:
        print(f"Đang lấy dữ liệu trang {page}...")

        url = f"https://www.thegioididong.com/laptop#c=44&o=13&pi={page}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        products = soup.select("ul.listproduct li.item.__cate_44")
        if not products:
            print("Không còn sản phẩm, dừng lấy dữ liệu.")
            break

        for product in products:
            a_tag = product.find("a", class_="main-contain")
            if not a_tag:
                continue

            href = a_tag["href"].strip() if "href" in a_tag.attrs else ""
            product_id = href.split("/")[-1] if href else "Không có ID"
            product_url = f"https://www.thegioididong.com{href}" if href else "Không có URL"

            name = product.find("h3").text.strip() if product.find("h3") else "Không có tên"
            price = product.find("strong").text.strip() if product.find("strong") else "Không có giá"
            desc = product.find("p").text.strip() if product.find("p") else "Không có mô tả"

            specs_div = product.find("div", class_="item-compare gray-bg")
            specs = " | ".join(span.text.strip() for span in specs_div.find_all("span")) if specs_div else "Không có thông số"

            detailed_specs = "Không có dữ liệu"
            product_response = requests.get(product_url, headers=HEADERS)
            product_soup = BeautifulSoup(product_response.text, "html.parser")

            spec_divs = product_soup.find_all("div", class_="box-specifi")
            if spec_divs:
                detailed_specs = []
                for spec in spec_divs:
                    category = spec.find("h3").text.strip() if spec.find("h3") else "Không có danh mục"
                    details = []
                    for li in spec.find_all("li"):
                        key = li.find("strong").text.strip() if li.find("strong") else "Không có tên"
                        span_tag = li.find("span")
                        a_tag = li.find("a")
                        if a_tag:
                            value = a_tag.text.strip()
                        elif span_tag:
                            value = span_tag.text.strip()
                        else:
                            value = "Không có giá trị"
                        details.append(f"{key}: {value}")
                    detailed_specs.append(f"{category}: " + " | ".join(details))
                detailed_specs = "\n".join(detailed_specs)

            f.write(f"ID: {product_id}\n")
            f.write(f"URL: {product_url}\n")
            f.write(f"Tên: {name}\n")
            f.write(f"Giá: {price}\n")
            f.write(f"Mô tả: {desc}\n")
            f.write(f"Thông số: {specs}\n")
            f.write(f"Thông số chi tiết:\n{detailed_specs}\n")
            f.write("=" * 50 + "\n")

            time.sleep(1)

        page += 1

# print("Đã lưu toàn bộ dữ liệu vào product_data.txt")
