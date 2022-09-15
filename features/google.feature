Feature: google search

  Scenario: sample test
    When open page /
    When click start_page_images_link
    When enter value Alpine cows in img_page_search_field
    When click img_page_search_button
    When click img_page_first_result
    When wait 5

