class TestDefaultRoutesAPI:
    """
    Ensure that the default routes are working as expected.

    Use full use-case stack dependency injection validate the default routes.
    """

    async def test_health_check_endpoint(self, test_client):
        resp = await test_client.get("/api/v1/health-check/")
        data = resp.json()

        assert resp.status_code == 200
        assert data["status"] == "ok"

    async def test_openapi_endpoint(self, test_client):
        resp = await test_client.get("/docs")
        assert resp.status_code == 200
