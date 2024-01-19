
role_options =["Data-user","Data-admin","System-super-admin"]


data_user_privileges =["openapi","static-offline-docs","custom_swagger_ui_html","swagger_ui_redirect","redoc_html","document",
                        "chat","search_engine_chat","chat_feedback","knowledge_base_chat","file_chat","agent_chat",
                        "list_kbs","list_files","search_docs","list_running_models","list_config_models","get_model_config",
                        "change_llm_model","get_server_configs","list_search_engines","get_server_prompt_template",
                        "completion","embed_texts_endpoint","user_login"]


data_admin_privileges = data_user_privileges + ["create_kb","delete_kb","update_docs_by_id","upload_docs","delete_docs",
                         "update_info","update_docs","download_doc","recreate_vector_store","upload_temp_docs","summary_file_to_vector_store","summary_doc_ids_to_vector_store",
                         "recreate_summary_vector_store"]


system_super_admin_privileges = data_admin_privileges + ["stop_llm_model","user_register","get_all_routes","search_users","update_user_info"]

role_privileges = {
    "Data-user": data_user_privileges,
    "Data-admin": data_admin_privileges,
    "System-super-admin": system_super_admin_privileges,
}

if __name__ == '__main__':
    print(data_admin_privileges)