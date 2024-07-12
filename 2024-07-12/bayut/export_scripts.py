from pipeline import MongoConnection
import csv
import logging

class ExportData:
    def __init__(self, output_csv_path):
        self.mongo_connection = MongoConnection()
        self.product_collection = self.mongo_connection.db["bayut_product_data"]
        self.documents = self.product_collection.find()
        self.output_csv_path = output_csv_path
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def data_document(self):

        headers = ['Url','Property_name','Property_id','Breadcrumbs','Price','Image_url','Description','Seller_name','Location','Property_type','Bathrooms','Bedrooms']
        
        with open(self.output_csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(headers)

            for doc in self.documents:
                
                url = doc.get('url','')
                property_name = doc.get('property_name','')
                property_id = doc.get('property_id','')
                breadcrumbs = doc.get('breadcrumbs','')
                price = doc.get('price','')
                image_url = doc.get('image_url','')
                description = doc.get('description','')
                seller_name = doc.get('seller_name','')
                location = doc.get('location','')
                property_type = doc.get('property_type','')
                bathrooms = doc.get('bathrooms','')
                bedrooms = doc.get('bedrooms','')

                data = [
                    url,
                    property_name,
                    property_id,
                    breadcrumbs,
                    price,
                    image_url,
                    description,
                    seller_name,
                    location,
                    property_type,
                    bathrooms,
                    bedrooms
                ]

                writer.writerow(data)
                logging.info(f"data saved to {self.output_csv_path}")

if __name__ == "__main__":

    obj = ExportData("bayut_2025_07_11.csv")
    obj.data_document()       