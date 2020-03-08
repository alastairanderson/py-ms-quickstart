from bs4 import BeautifulSoup
from urllib.parse import unquote

class HtmlUtils:

    @staticmethod
    def extract_main_content(html_content: str, content_element: dict):
        '''Returns the main content area of an article from the HTML 
        page. If multiple elements and attributes are specified, each 
        combination of them are tried until content is found. If no
        content is found 

        :param html_content: the raw html page downloaded.

        :param content_element: the identifying HTML elements of the main 
            content (e.g. div, article). The dictionary contains a single
            key-value pair. The key is the element name, and the value
            are identifying attributes
        '''
        soup = BeautifulSoup(html_content, "lxml")
        main_content = None

        for key in content_element.keys():
            main_content = soup.find(key, attrs=content_element[key])

            if main_content:
                return main_content

        return None


    @staticmethod
    def extract_content_elements(content: dict, content_identifier: dict):
        '''Returns unique values of element attributes from html content.
            if a content_element

        :param content: the html content to extract the element attributes from

        :param content_identifier: the identifying HTML element to extract.
            Can contain child_elements, and also return_attribute.
            if a return_attribute and child_elements both exist at the 
            same level, if an attribute matching the return_attribute
            is found, this is returned and the child_elements are 
            ignored
        '''
        result = []  

        if not content_identifier["element"]:
            raise Exception(f"No element name specified in {content_identifier}")

        all_elements = content.find_all(content_identifier["element"], attrs=content_identifier["attributes"])

        # typically if we want to return a list of HTML elements, and not specific values within it
        if "return_attribute" not in content_identifier and "child_element" not in content_identifier:
            return all_elements

        if all_elements:
            for element in all_elements:
                if "return_attribute" in content_identifier:
                    for attribute in content_identifier["return_attribute"]:
                        attribute_value = element.get(attribute)
                        if attribute_value:
                            result.append(attribute_value)

                if len(result) > 0:
                    continue  # if attribute found, move to next element

                if "child_element" in content_identifier:  # first-level child_element's
                    if "element" in content_identifier["child_element"]:
                        if "attributes" in content_identifier["child_element"]:
                            child_elements_1 = element.find_all(content_identifier["child_element"]["element"], attrs=content_identifier["child_element"]["attributes"])
                        else:
                            child_elements_1 = element.find_all(content_identifier["child_element"]["element"])

                    if child_elements_1:
                        for child_element in child_elements_1:
                            if "return_attribute" in content_identifier["child_element"]:
                                for attribute in content_identifier["child_element"]["return_attribute"]:
                                    attribute_value = child_element.get(attribute)
                                    if attribute_value:
                                        result.append(attribute_value)

        return list(set(result)) # all elements processed and duplicates removed


    # @staticmethod
    # def extract_all_links(content: dict):
    #     return HtmlUtils.extract_content_elements(content, None, {'a': 'href'})

    # def extract_images_from_article(content: dict):
    #     result = HtmlUtils.extract_content_elements(content, None, {'img': 'src', 'img': 'srcset', 'img': 'data-srcset'})
    #     # result = HtmlUtils.extract_content_elements(content, 'figure', {}