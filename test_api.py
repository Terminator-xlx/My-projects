import requests
import pytest
from typing import Dict, Any


class TestAdvancedAPI:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    @pytest.fixture
    def auth_headers(self):
        """Фикстура для заголовков авторизации"""
        return {
            'Authorization': 'Bearer your-token-here',
            'Content-Type': 'application/json'
        }

    @pytest.fixture
    def sample_post_data(self):
        """Фикстура с тестовыми данными"""
        return {
            "title": "Test Post Title",
            "body": "Test post body content",
            "userId": 1
        }

    @pytest.mark.parametrize("post_id,expected_status", [
        (1, 200),
        (100, 200),
        (0, 404),  # Несуществующий ID
        (-1, 404),  # Невалидный ID
    ])
    def test_get_post_with_different_ids(self, post_id, expected_status):
        """Параметризованный тест для разных ID постов"""
        response = requests.get(f"{self.BASE_URL}/posts/{post_id}")
        assert response.status_code == expected_status

    def test_post_validation(self, sample_post_data, auth_headers):
        """Тест валидации при создании поста"""
        # Тест с неполными данными
        incomplete_data = {"title": "Only title"}
        response = requests.post(
            f"{self.BASE_URL}/posts",
            json=incomplete_data,
            headers=auth_headers
        )
        # Предполагаем, что API требует все поля, по факту не требует, потому что код 201 -успех
        assert response.status_code in [400, 422]  # Bad Request или Unprocessable Entity

    def test_response_time(self):
        """Тест времени ответа API"""
        import time

        start_time = time.time()
        response = requests.get(f"{self.BASE_URL}/posts")
        end_time = time.time()

        response_time = end_time - start_time

        assert response.status_code == 200
        assert response_time < 2.0  # Ответ должен приходить менее чем за 2 секунды

    def test_pagination(self):
        """Тест пагинации"""
        response = requests.get(f"{self.BASE_URL}/posts?_page=1&_limit=5")

        assert response.status_code == 200
        posts = response.json()

        # Проверяем, что количество постов соответствует лимиту
        assert len(posts) <= 5

        # Проверяем заголовки пагинации (если API их предоставляет)
        if 'Link' in response.headers:
            assert 'rel="next"' in response.headers['Link']