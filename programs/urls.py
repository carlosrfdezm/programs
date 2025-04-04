from django.urls import path


from . import views
from . import cgc_views as cgc_views

app_name = 'programs'

urlpatterns = [
    path('', views.index, name='index'),
    path('comments/<int:thesis_id>/new', views.new_phd_thesis_comment, name='new_phd_thesis_comment'),
    path('edit', views.edit_program, name='edit_program'),
    path('home/', views.home, name='home'),
    path('background/<int:background_id>', views.program_background, name='program_background'),
    #Path de estudiantes de doctorados, excepto la lista
    path('students/create', views.create_student, name='create_student'),
    path('students/list/<str:scope>', views.students_list, name='students_list'),
    path('students/csv/export/<str:scope>', views.export_csv_students, name='export_csv_students'),
    path('students/<int:student_id>/edit', views.edit_student, name='edit_student'),
    path('students/<int:student_id>/thesis/new', views.ajx_new_phd_thesis, name='ajx_new_phd_thesis'),
    path('students/<int:student_id>/thesis/remove', views.ajx_rm_phd_thesis, name='ajx_rm_phd_thesis'),
    path('students/<int:student_id>/profile', views.view_student_profile, name='view_student_profile'),
    path('students/<int:student_id>/autoedit/profile', views.autoedit_student_profile, name='autoedit_student_profile'),
    path('students/<int:student_id>/picture', views.program_student_picture, name='program_student_picture'),
    path('students/<int:student_id>/evaluate', views.evaluate_student, name='evaluate_student'),
    path('students/<int:student_id>/evaluations', views.student_evals, name='student_evals'),
    path('students/<int:student_id>/print/evals', views.print_student_evals, name='print_student_evals'),
    path('students/<int:student_id>/plan/create', views.create_formation_plan, name='create_formation_plan'),
    path('students/<int:student_id>/plan/edit', views.edit_formation_plan, name='edit_formation_plan'),
    path('students/<int:student_id>/plan/view', views.view_formation_plan, name='view_formation_plan'),
    path('students/<int:student_id>/plan/print', views.print_student_plan, name='print_student_plan'),
    path('students/<int:student_id>/file/<int:doc_id>/view', views.student_filedoc_view, name='student_filedoc_view'),

    #Paths de estudiantes de maestria
    path('', views.msc_index, name='msc_index'),
    path('msc/<int:edition_id>/students/create', views.create_msc_student, name='create_msc_student'),
    path('msc/<int:edition_id>/students/<int:student_id>/edit', views.edit_msc_student, name='edit_msc_student'),
    path('msc/edition/<int:edition_id>/students/<str:scope>/list', views.msc_edition_students_list, name='msc_edition_students_list'),
    path('msc/students/<str:scope>/list', views.msc_all_students_list, name='msc_all_students_list'),
    

    path('', views.dip_index, name='dip_index'),
    path('dip/<int:edition_id>/students/create', views.create_dip_student, name='create_dip_student'),
    path('dip/<int:edition_id>/students/<int:student_id>/edit', views.edit_dip_student, name='edit_dip_student'),
    path('dip/edition/<int:edition_id>/students/<str:scope>/list', views.dip_edition_students_list, name='dip_edition_students_list'),
    path('dip/students/<str:scope>/list', views.dip_all_students_list, name='dip_all_students_list'),

    path('professors/create', views.create_professor, name='create_professor'),
    path('professors/<int:member_id>/edit', views.edit_member, name='edit_member'),
    path('professors/<int:member_id>/picture', views.program_member_picture, name='program_member_picture'),
    path('professors/<str:scope>/list', views.members_list, name='members_list'),
    path('professors/<int:member_id>/view/profile', views.view_program_member_profile, name='view_program_member_profile'),
    path('professors/<int:member_id>/autoedit/profile', views.autoedit_member_profile, name='autoedit_member_profile'),

    path('lines/create', views.create_line, name='create_line'),
    path('lines/list', views.program_lines, name='program_lines'),
    path('lines/<int:line_id>/students', views.students_by_line, name='students_by_line'),
    path('lines/<int:line_id>/edit', views.edit_line, name='edit_line'),

    path('projects/create', views.create_project, name='create_project'),
    path('projects/<int:project_id>/edit', views.edit_project, name='edit_project'),
    path('projects/list', views.projects_list, name='projects_list'),

    path('editions/create',views.create_program_edition, name='create_program_edition'),
    path('editions/list',views.editions_list, name='editions_list'),
    path('editions/<int:edition_id>/edit',views.edit_program_edition, name='edit_program_edition'),
    path('editions/<int:edition_id>/course/create',views.create_edition_course, name='create_edition_course'),
    path('editions/<int:edition_id>/courses',views.edition_courses, name='edition_courses'),
    path('editions/<int:edition_id>/courses/print',views.print_edition_courses_registers, name='print_edition_courses_registers'),

    path('courses/create', views.create_program_course, name='create_program_course'),
    path('courses/list', views.program_courses, name='program_courses'),
    path('courses/<int:course_id>/edit', views.edit_program_course, name='edit_program_course'),
    path('courses/<int:course_id>/print/register', views.print_course_register, name='print_course_register'),


    path('ajx/document/file/update', views.ajx_update_filedoc, name='ajx_update_filedoc'),
    path('ajx/document/file/upgrade', views.ajx_upgrade_filedoc, name='ajx_upgrade_filedoc'),
    path('ajx/document/file/delete', views.ajx_delete_filedoc, name='ajx_delete_filedoc'),

    path('ajx/user/exists', views.ajx_usr_exists, name='ajx_usr_exists'),
    path('ajx/member/exists', views.ajx_program_member_tuthor, name='ajx_program_member_tuthor'),
    path('ajx/student/delete', views.ajx_delete_student, name='ajx_delete_student'),
    path('ajx/student/autorequest', views.ajx_auto_request, name='ajx_auto_request'),
    path('ajx/member/delete', views.ajx_delete_member, name='ajx_delete_member'),
    path('ajx/tuthor/delete', views.ajx_delete_tuthor, name='ajx_delete_tuthor'),

    path('ajx/student/<int:student_id>/tuthor/create', views.ajx_create_tuthor, name='ajx_create_tuthor'),
    path('ajx/student/<int:student_id>/plan/activity/add', views.ajx_create_activity, name='ajx_create_activity'),
    path('ajx/student/<int:student_id>/plan/activity/edit', views.ajx_edit_activity, name='ajx_edit_activity'),
    path('ajx/student/<int:student_id>/plan/activity/delete', views.ajx_delete_activity, name='ajx_delete_activity'),
    path('ajx/student/exists', views.ajx_student_exists, name='ajx_student_exists'),

    path('ajx/line/delete', views.ajx_delete_line, name='ajx_delete_line'),
    path('ajx/line/projects', views.ajx_line_projects, name='ajx_line_projects'),
    path('ajx/edition/delete', views.ajx_delete_program_edition, name='ajx_delete_program_edition'),
    path('ajx/project/delete', views.ajx_delete_project, name='ajx_delete_project'),

    path('ajx/statistics/thisyear/requests', views.ajx_this_year_requests, name='ajx_this_year_requests'),
    path('ajx/statistics/byyear/requests', views.ajx_by_year_requests, name='ajx_by_year_requests'),
    path('ajx/statistics/lastyear/requests', views.ajx_last_years_requests, name='ajx_last_years_requests'),
    path('ajx/statistics/students/status', views.ajx_students_by_state, name='ajx_students_by_state'),
    path('ajx/statistics/students/gender', views.ajx_students_by_sex, name='ajx_students_by_sex'),
    path('ajx/statistics/students/<str:scope>/line', views.ajx_students_by_line, name='ajx_students_by_line'),
    path('ajx/statistics/students/line/donut', views.ajx_students_by_line_donut, name='ajx_students_by_line_donut'),
    path('ajx/statistics/students/category', views.ajx_students_by_category, name='ajx_students_by_category'),
    path('ajx/statistics/students/country', views.ajx_students_by_country, name='ajx_students_by_country'),
    path('ajx/statistics/students/age', views.ajx_students_by_age, name='ajx_students_by_age'),
    path('ajx/statistics/students/editions', views.ajx_students_by_edition, name='ajx_students_by_edition'),
    path('ajx/statistics/students/graduated/editions', views.ajx_graduated_by_edition, name='ajx_graduated_by_edition'),
    path('ajx/statistics/members/degree', views.ajx_members_by_grade, name='ajx_members_by_grade'),
    path('ajx/statistics/members/age', views.ajx_members_by_age, name='ajx_members_by_age'),
    path('ajx/statistics/next/defenses', views.ajx_next_years_defenses, name='ajx_next_years_defenses'),

    path('ajx/messages/members/personal', views.ajx_member_personal_msg, name='ajx_member_personal_msg'),
    path('ajx/messages/members/massive', views.ajx_member_massive_msg, name='ajx_member_massive_msg'),
    path('ajx/messages/massive/all', views.ajx_all_massive_msg, name='ajx_all_massive_msg'),
    path('ajx/messages/students/personal', views.ajx_student_personal_msg, name='ajx_student_personal_msg'),
    path('ajx/messages/students/massive', views.ajx_students_massive_msg, name='ajx_students_massive_msg'),
    path('ajx/messages/everybody/massive', views.ajx_everybody_massive_msg, name='ajx_everybody_massive_msg'),
    path('ajx/messages/mark/readed', views.ajx_mark_message_readed, name='ajx_mark_message_readed'),
    path('ajx/messages/delete', views.ajx_delete_message, name='ajx_delete_message'),

    path('ajx/program/brieffing/delete', views.ajx_delete_program_document, name='ajx_delete_program_document'),
    path('ajx/program/background/new', views.ajx_upload_background, name='ajx_upload_background'),
    path('ajx/program/background/delete', views.ajx_delete_bg, name='ajx_delete_bg'),
    path('ajx/program/background/edit', views.ajx_edit_background, name='ajx_edit_background'),

    path('ajx/course/delete', views.ajx_delete_course, name='ajx_delete_course'),
    path('ajx/evaluation/edit', views.ajx_edit_eval, name='ajx_edit_eval'),
    path('ajx/evaluation/delete', views.ajx_delete_eval, name='ajx_delete_eval'),
    path('ajx/edition/<int:edition_id>/courses/import', views.ajx_import_courses, name='ajx_import_courses'),
    path('ajx/edition/courses/professor/delete', views.ajx_delete_course_professor, name='ajx_delete_course_professor'),
    path('ajx/speciality/delete', views.ajx_delete_speciality, name='ajx_delete_speciality'),
    path('ajx/student/<int:student_id>/activity/status/change', views.ajx_change_activity_status, name='ajx_change_activity_status'),
    path('ajx/new/delete', views.ajx_delete_new, name='ajx_delete_new'),
    path('ajx/announcement/delete', views.ajx_delete_announcement, name='ajx_delete_announcement'),
    path('ajx/comment/delete', views.ajx_rm_phd_thesis_comment, name='ajx_rm_phd_thesis_comment'),
    path('ajx/faq/delete', views.ajx_delete_faq, name='ajx_delete_faq'),

    path('ajx/requirenment/<str:scope>/create', views.ajx_new_requirenment, name='ajx_new_requirenment'),
    path('ajx/requirenment/delete', views.ajx_delete_r, name='ajx_delete_r'),
    path('ajx/requirenment/data', views.ajx_r_data, name='ajx_r_data'),
    path('ajx/requirenment/edit', views.ajx_edit_requirenment, name='ajx_edit_requirenment'),


    path('statistics', views.program_statistics, name='program_statistics'),
    path('documents/create', views.create_program_doc, name='create_program_doc'),
    path('documents/<int:doc_id>/edit', views.edit_program_doc, name='edit_program_doc'),
    path('documents/<int:doc_id>/view', views.program_doc_view, name='program_doc_view'),
    path('documents/<int:doc_id>/public/view', views.public_program_doc_view, name='public_program_doc_view'),
    path('documents/list', views.program_documents, name='program_documents'),
    path('documents/cgc', views.program_cgc_documents, name='program_cgc_documents'),
    path('documents/cgc/<int:document_id>/view', views.program_cgc_document_view, name='program_cgc_document_view'),
    path('documents/download', views.program_download_docs, name='program_download_docs'),
    path('documents/year/<int:year>/list', views.program_docs_by_year, name='program_docs_by_year'),
    path('documents/year/<int:year>/download', views.program_by_year_doc_download, name='program_by_year_doc_download'),

    path('reports', views.docx_program_report, name='docx_program_report'),


    path('speciality/create', views.create_phd_speciality, name='create_phd_speciality'),
    path('speciality/list', views.phd_specialities, name='phd_specialities'),
    path('speciality/<int:speciality_id>/edit', views.edit_phd_speciality, name='edit_phd_speciality'),

    path('new/<int:new_id>/picture', views.program_new_picture, name='new_img'),
    path('new/<int:new_id>/read', views.read_new, name='read_new'),
    path('new/<int:new_id>/edit', views.edit_new, name='edit_new'),
    path('new/create', views.create_new, name='create_new'),
    path('news/list', views.news_list, name='news_list'),

    path('faq/<int:faq_id>/read', views.read_faq, name='read_faq'),
    path('faq/<int:faq_id>/edit', views.edit_faq, name='edit_faq'),
    path('faq/create', views.create_faq, name='create_faq'),
    path('faq/list', views.faq_list, name='faq_list'),


    path('request/confirm/<str:request_id>', views.confirm_auto_request, name='request_confirm'),

    # Paths de convocatorias
    path('announcement/student/<int:student_id>/new', views.new_phd_announcement, name='new_phd_announcement'),
    path('announcements/list', views.program_annoucements, name='program_announcements'),
    path('announcements/<int:announcement_id>/edit', views.edit_phd_announcement, name='edit_phd_announcement'),
    path('announcements/<int:announcement_id>/pdf', views.download_announcement_pdf, name='download_announcement_pdf'),

    path('thesis/<int:thesis_id>/new/comment', views.ajx_new_phd_thesis_comment, name='ajx_new_phd_thesis_comment'),
    path('thesis/<int:thesis_id>/download/comments', views.docx_thesis_comments, name='docx_thesis_comments'),
    path('thesis/<int:thesis_id>/comments', views.phd_thesis_comments, name='phd_thesis_comments'),

    path('evidences/download', views.download_evidences , name='download_evidences'),



    # path('login', views.mylogin, name='my_login'),
    # path('logout/<str:court_slug>/', views.mylogout, name='my_logout'),
    # path('cngc/member/<int:member_id>/pic', views.cngc_member_picture, name='cngc_member_picture'),

]
