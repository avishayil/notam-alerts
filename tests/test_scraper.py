from src.scraper import NotamScraper


def test_scrape_returns_list():
    scraper = NotamScraper()
    result = scraper.scrape()
    assert isinstance(result, list)
    if result:
        assert "notam_id" in result[0]
        assert "start_il" in result[0]
        assert "end_il" in result[0]
