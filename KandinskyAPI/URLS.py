class ApiUrls:
    base_url = 'https://api-key.fusionbrain.ai/key/api/v1/'
    text2image_styles = 'https://cdn.fusionbrain.ai/static/styles/api'

    text2image_run_url = f'{base_url}text2image/run'
    text2image_status_url = f'{base_url}text2image/status/$uuid'

    text2image_models_url = f'{base_url}models'
