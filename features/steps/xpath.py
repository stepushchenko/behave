xpath = {

    'start_page_sign_in_button': "//*[@data-test-id='auth.button.sign_in']",
    'start_page_sign_up_button': "//*[@data-test-id='auth.button.sign_up']",

    'sign_up_page_email_input': "//*[@data-test-id='auth.input.email']",
    'sign_up_page_send_code_button': "//*[@data-test-id='auth.button.send_code']",
    'sign_up_page_agree_checkbox': "//*[@data-test-id='auth.checkbox.agree']",
    'sign_up_page_error': "//*[@data-test-id='auth.text.sign_up_error']",
    'sign_up_page_code_input': "//*[@data-test-id='auth.input.code']",
    'sign_up_page_error_popup': "//*[@data-test-id='auth.alert.error.message']",
    'sign_up_page_email_error': "//input[@placeholder='email@example.com']/following::span",

    'sign_in_page_email_input': "//*[@data-test-id='auth.input.email']",
    'sign_in_page_email_error': "//input[@placeholder='email@example.com']/following::span",
    'sign_in_page_send_code_button': "//*[@data-test-id='auth.button.send_code']",
    'sign_in_page_code_input': "//*[@data-test-id='auth.input.code']",
    'sign_in_page_error_popup': "//*[@data-test-id='auth.alert.error.message']",

    'header_profile_icon': "//div[@class='TopMenuLayout']/div[1]/div[2]/div[3]",
    'header_profile_menu_logout': "//*[contains(text(), 'Logout')]",
    'header_profile_menu_my_profile': "//*[contains(text(), 'My Profile')]",
    'header_notifications_icon': "//div[@class='TopMenuLayout']/div[1]/div[2]/div[2]",

    'menu_yourspace_page': "//ul[@class='navbarNav']//a[@href='/your-space']",
    'menu_community': "//*[@data-test-id='main_menu.button.community']",

    'yourspace_page_h1': "//*[@data-test-id='dashboard.block.h1']",
    'yourspace_page_avatar': "//div[contains(@class,'MyProfileImg')]//div[contains(@class,'UserProfileImg')]/img",
    'yourspace_page_library_tab': "//*[@data-test-id='dashboard.button.library']",
    'yourspace_page_toolbox_tab': "//*[@data-test-id='dashboard.button.toolbox']",
    'yourspace_page_services_tab': "//*[@data-test-id='dashboard.button.services']",
    'yourspace_page_finances_tab': "//*[@data-test-id='dashboard.button.finances']",
    'yourspace_page_session_notes_tab': "//*[@data-test-id='dashboard.button.session_notes']",
    'yourspace_page_practice_link': "//*[@data-test-id='dashboard.link.to_practice']",
    'yourspace_page_edit_profile_button': "//*[@data-test-id='my_profile.button.edit_profile']",

    'community_page_search_field': "//div[contains(@class, 'Coaches')]//input[@id='search']",
    'community_page_practice_block': "//div[contains(@class, 'Practice')]",

    'profile_page_edit_practice_button': "//*[@data-test-id='edit_profile.button.edit_practice']",
    'profile_page_profile_picture': "//div[@class='UserProfile']//div[contains(@class,'AvatarPlaceholder')]",
    'profile_page_save_button': "//*[@data-test-id='edit_profile.button.save']",

    'practice_page_certificates_button': "//*[@data-test-id='practice.button.certificates']",
    'practice_page_availability_button': "//*[@data-test-id='practice.button.availability']",
    'practice_page_add_program_button': "//*[@data-test-id='dashboard.button.add_program']",
    'practice_page_cover': "//div[contains(@class, 'HeaderImg')]//img",

    'create_program_page_cover_icon': "//*[@data-test-id='create_program_description.button.cover']",
    'create_program_page_title': "//*[@data-test-id='create_program_description.input.title']",
    'create_program_page_description': "//*[@data-test-id='create_program_description.input.description']",
    'create_program_page_continue_button': "//*[@data-test-id='create_program.button.continue']",
    'create_program_page_group_type_button': "//*[@data-test-id='create_program_details.block.program_type.group']",
    'create_program_page_individual_type_button': "//*[@data-test-id='create_program_details.block.program_type.individual']",
    'create_program_page_evergreen_selector': "//h3[contains(text(), 'Evergreen program')]/div",
    'create_program_custom_amount_button': "//p[contains(text(),'Custom amount')]",
    'create_program_price_input': "//input[@placeholder='$1 - $10000']",
    'create_program_paid_elsewhere_selector': "//div[contains(@class, 'Switch')]//label",

    'program_page_title': "//div[contains(@class, 'SeeProgram')]//h1",
    'program_page_price': "//div[contains(@class, 'SeeProgram')]//h1/following::div",
    'program_page_delete_button': "//div[contains(@class, 'CoachRightMenu')]//div[contains(text(), 'Delete Program')]",
    'program_page_delete_program_popup_yes_button': "//h1[contains(text(), 'Delete the program?')]/following::div/div[contains(text(), 'Yes')]",
    'program_page_status': "//div[contains(@class, 'SeeProgram')]//div[contains(@class, 'OverlayImage')]/following::div",
    'program_page_publish_button': "//*[@data-test-id='see_program.button.publish']",
    'program_page_description_tab': "//div[contains(@class, 'SeeProgram')]//div[contains(text(), 'Description')]",
    'program_page_description_tab_description': "//div[contains(@class, 'DescriptionTab')]",

    'select_file_popup_upload_input': "//*[@data-test-id='addFile.input.file']",
    'select_file_popup_select_file_button': "//*[@data-test-id='addFile.button.confirm']",

    'popup_close_button': "//div[contains(@class, 'ModalWindowContainer')]/button[contains(@class, 'closeBut')]",

    'add_certificate_popup_close_button': "//div[contains(text(),'Add certificate')]/following::button",

    'edit_practice_popup_cover': "//*[@data-test-id='edit_coach_profile.button.add_cover']",
    'edit_practice_popup_save_button': "//*[@data-test-id='edit_coach_profile.button.save']/span",

    'certificates_popup_add_certificate_button': "//*[@data-test-id='certificate.button.show_add_modal']",
    'certificates_popup_close_button': "//div[contains(text(),'Certificates')]/following::button[@data-test-id='modal.button.close']",
}
