from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from pyhearthis.hearthis import HearThis
from tests import mocks
from tests import response_data


class HearThisTests(IsolatedAsyncioTestCase):

    async def test_that_login_returns_expected_data(self):
        # Arrange
        mock = AsyncMock()
        mock.get = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/login",
            'login_response.json',
            email="mymail@test.de",
            password="mypassword"
        )
        sut = HearThis(mock)

        # Act
        result = await sut.login("mymail@test.de", "mypassword")

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.username, "mymail")
        self.assertEqual(result.id, 12345678)

    async def test_that_get_feeds_returns_expected_data(self):
        # Arrange
        mock = AsyncMock()
        mock.get = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/feed/",
            'get_feeds_response.json',
            key="mykey",
            secret="mysecret",
            page="1",
            count="5"
        )
        user = mocks.create_logged_in_user()
        sut = HearThis(mock)

        # Act
        result = await sut.get_feeds(user)

        # Assert
        self.assertIsNotNone(result)
        feed = result[0]
        self.assertEqual(
            feed.title, "Shawne @ Back To The Roots 2 (05.07.2014)")
        self.assertIsNotNone(feed.user.username)
        self.assertEqual(feed.id, 48250)

    async def test_that_get_categories_returns_expected_data(self):
        # Arrange
        mock = AsyncMock()
        mock.get = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/categories/", 'get_categories.json')
        sut = HearThis(mock)

        # Act
        result = await sut.get_categories()

        # Assert
        self.assertIsNotNone(result)
        category = result[0]
        self.assertEqual(category.id, "acoustic")
        self.assertEqual(category.name, "Acoustic")

    async def test_that_get_waveform_data_returns_expected_data(self):
        # Arrange
        client_session_mock = AsyncMock()
        client_session_mock.get = mocks.RequestContextManagerMock.with_return_value(
            "https://waveform.data", response_data.WAVEFORM_RESPONSE_DATA)
        track = mocks.create_single_track()
        sut = HearThis(client_session_mock)

        # Act
        result = await sut.get_waveform_data(track)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result, response_data.WAVEFORM_RESPONSE_DATA)

    async def test_that_get_category_tracks_returns_expected_data(self):
        # Arrange
        client_session_mock = AsyncMock()
        client_session_mock.get = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/categories/drumandbass",
            'get_genre_list_response.json',
            key="mykey",
            secret="mysecret",
            page="1",
            count="5"
        )
        user = mocks.create_logged_in_user()
        category = mocks.create_category()
        sut = HearThis(client_session_mock)

        # Act
        result = await sut.get_category_tracks(user, category)

        # Assert
        self.assertIsNotNone(result)
        feed = result[0]
        self.assertEqual(
            feed.title, "Shawne @ Back To The Roots 2 (05.07.2014)")
        self.assertEqual(feed.id, 48250)
        self.assertIsNotNone(feed.user.username)

    async def test_that_api_receives_expected_data_when_create_playlist(self):
        # Arrange
        client_session_mock = AsyncMock()
        client_session_mock.post = mocks.RequestContextManagerMock
        user = mocks.create_logged_in_user()
        sut = HearThis(client_session_mock)

        # Act
        await sut.create_playlist(user, "MyNewPlaylist")

        # Assert
        posted_data = mocks.RequestContextManagerMock.pop_post_data_for_url(
            "https://api-v2.hearthis.at/set_ajax_add.php")
        expected_data = {
            'action': 'createnew',
            'key': 'mykey',
            'secret': 'mysecret',
            'new_set': 'MyNewPlaylist',
            'privat': 1,
            'sort_config': 1
        }

        self.assertDictEqual(expected_data, posted_data)

    async def test_that_get_playlists_returns_expected_data(self):
        # Arrange
        client_session_mock = AsyncMock()
        client_session_mock.get = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/mymail-oc",
            'get_playlists_response.json',
            key="mykey",
            secret="mysecret",
            page="1",
            count="5",
            type="playlists"
        )
        user = mocks.create_logged_in_user()
        sut = HearThis(client_session_mock)

        # Act
        result = await sut.get_playlists(user)

        # Assert
        self.assertIsNotNone(result)
        playlist = result[0]
        self.assertEqual(playlist.id, 438)
        self.assertEqual(playlist.title, "Back In Time")
        self.assertIsNotNone(playlist.user.username)

    async def test_that_api_receives_expected_data_when_add_track_to_playlist(self):
        # Arrange
        client_session_mock = AsyncMock()
        client_session_mock.post = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/set_ajax_add.php", 'single_playlist.json')
        user = mocks.create_logged_in_user()
        track = mocks.create_single_track()
        playlist = mocks.create_playlist()
        sut = HearThis(client_session_mock)

        # Act
        await sut.add_track_to_playlist(user, track, playlist)

        # Assert
        posted_data = mocks.RequestContextManagerMock.pop_post_data_for_url(
            "https://api-v2.hearthis.at/set_ajax_add.php")
        expected_data = {
            'action': 'add',
            'key': 'mykey',
            'secret': 'mysecret',
            'track_id': 48250,
            'set': 438
        }

        self.assertDictEqual(expected_data, posted_data)

    async def test_that_api_receives_expected_data_when_add_track_to_new_playlist(self):
        # Arrange
        client_session_mock = AsyncMock()
        client_session_mock.post = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/set_ajax_add.php", 'single_playlist.json')
        user = mocks.create_logged_in_user()
        track = mocks.create_single_track()
        sut = HearThis(client_session_mock)

        # Act
        await sut.add_track_to_new_playlist(user, track, 'my_new_playlist')

        # Assert
        posted_data = mocks.RequestContextManagerMock.pop_post_data_for_url(
            "https://api-v2.hearthis.at/set_ajax_add.php")
        expected_data = {
            'action': 'add',
            'key': 'mykey',
            'secret': 'mysecret',
            'track_id': 48250,
            'new_set': 'my_new_playlist'
        }

        self.assertDictEqual(expected_data, posted_data)

    async def test_that_get_playlist_tracks_returns_expected_data(self):
        # Arrange
        client_session_mock = AsyncMock()
        playlist = mocks.create_playlist()
        client_session_mock.get = mocks.RequestContextManagerMock.with_json_response(
            f"https://api-v2.hearthis.at/set/{playlist.permalink}/",
            'get_playlist_tracks_response.json',
            key="mykey",
            secret="mysecret"
        )
        user = mocks.create_logged_in_user()
        sut = HearThis(client_session_mock)

        # Act
        result = await sut.get_playlist_tracks(user, playlist)

        # Assert
        self.assertIsNotNone(result)
        first_track = result[0]
        self.assertEqual(first_track.id, 12345)
        self.assertEqual(first_track.title, "The Souled Out Show August 27th")
        self.assertIsNotNone(first_track.user.username)

    async def test_that_api_receives_expected_data_when_delete_track_from_playlist(self):
        # Arrange
        client_session_mock = AsyncMock()
        client_session_mock.post = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/set_ajax_add.php", 'single_playlist.json')
        user = mocks.create_logged_in_user()
        playlist = mocks.create_playlist()
        track = mocks.create_single_track()
        sut = HearThis(client_session_mock)

        # Act
        result = await sut.delete_track_from_playlist(user, track, playlist)

        # Assert
        posted_data = mocks.RequestContextManagerMock.pop_post_data_for_url(
            "https://api-v2.hearthis.at/set_ajax_add.php")
        expected_data = {
            'action': 'deleteentry',
            'id': track.id,
            'key': 'mykey',
            'secret': 'mysecret',
            'set_id': playlist.id
        }

        self.assertDictEqual(expected_data, posted_data)
        self.assertIsNotNone(result)

    async def test_that_api_receives_expected_data_when_delete_playlist(self):
        # Arrange
        client_session_mock = AsyncMock()
        client_session_mock.post = mocks.RequestContextManagerMock.with_return_value(
            "https://api-v2.hearthis.at/set_ajax_edit.php", 'DELETED')
        user = mocks.create_logged_in_user()
        playlist = mocks.create_playlist()
        sut = HearThis(client_session_mock)

        # Act
        await sut.delete_playlist(user, playlist)

        # Assert
        posted_data = mocks.RequestContextManagerMock.pop_post_data_for_url(
            "https://api-v2.hearthis.at/set_ajax_edit.php")
        expected_data = {
            'action': 'delete',
            'key': 'mykey',
            'secret': 'mysecret',
            'set': playlist.id
        }

        self.assertDictEqual(expected_data, posted_data)

    async def test_that_search_returns_expected_data(self):
        # Arrange
        client_session_mock = AsyncMock()
        client_session_mock.get = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/search/",
            'search_response.json',
            key="mykey",
            secret="mysecret",
            t="MySearchQuery",
            page="1",
            count="5"
        )
        user = mocks.create_logged_in_user()
        sut = HearThis(client_session_mock)

        # Act
        result = await sut.search(user, "MySearchQuery")

        # Assert
        self.assertIsNotNone(result)
        feed = result[0]
        self.assertEqual(
            feed.title, "Shawne @ Back To The Roots 2 (05.07.2014)")
        self.assertEqual(feed.id, 48250)

    async def test_that_result_is_empty_when_limit_reached_response_occurs(self):
        # Arrange
        client_session_mock = AsyncMock()
        client_session_mock.get = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/search/",
            'limit_reached_response.json',
            key="mykey",
            secret="mysecret",
            t="House",
            page="1",
            count="5"
        )
        user = mocks.create_logged_in_user()
        sut = HearThis(client_session_mock)

        # Act
        result = await sut.search(user, "House")

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)

    async def test_that_expcetion_is_raised_when_count_excceeds_max_count(self):
        # Arrange
        client_session_mock = AsyncMock()
        client_session_mock.get = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/search/",
            'search_response.json',
            key="mykey",
            secret="mysecret",
            t="MySearchQuery",
            page="1",
            count="5"
        )
        user = mocks.create_logged_in_user()
        category = mocks.create_category()
        sut = HearThis(client_session_mock)

        # search
        with self.assertRaises(Exception) as context:
            await sut.search(user, "MySearchQuery", None, None, 1, 21)

        self.assertTrue(
            'maximum allowed pagecount is 20' in str(context.exception))

        # get_feeds
        with self.assertRaises(Exception) as context:
            await sut.get_feeds(user, "", None, None, 1, 21)

        self.assertTrue(
            'maximum allowed pagecount is 20' in str(context.exception))

        # get_category_tracks
        with self.assertRaises(Exception) as context:
            await sut.get_category_tracks(user, category, 0, 21)

        self.assertTrue(
            'maximum allowed pagecount is 20' in str(context.exception))

        # get_playlists
        with self.assertRaises(Exception) as context:
            await sut.get_playlists(user, 1, 21)

        self.assertTrue(
            'maximum allowed pagecount is 20' in str(context.exception))

        # get_playlists
        with self.assertRaises(Exception) as context:
            await sut.get_playlists(user, 1, 21)

        self.assertTrue(
            'maximum allowed pagecount is 20' in str(context.exception))

        # get_artist_tracks
        with self.assertRaises(Exception) as context:
            await sut.get_artist_tracks(user, "permalink", page=1, count=21)

        self.assertTrue(
            'maximum allowed pagecount is 20' in str(context.exception))

    async def test_that_search_result_user_is_accessible_by_properties(self):
        # Arrange
        client_session_mock = AsyncMock()
        client_session_mock.get = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/search/",
            'search_response.json',
            key="mykey",
            secret="mysecret",
            t="MySearchQuery",
            page="1",
            count="5"
        )
        user = mocks.create_logged_in_user()
        sut = HearThis(client_session_mock)

        # Act
        result = await sut.search(user, "MySearchQuery")

        # Assert
        user = result[0].user
        self.assertIsNotNone(user.username)

    async def test_that_playlist_user_is_accessible_by_properties(self):
        # Arrange
        client_session_mock = AsyncMock()
        client_session_mock.get = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/mymail-oc",
            'get_playlists_response.json',
            key="mykey",
            secret="mysecret",
            page="1",
            count="5",
            type="playlists"
        )
        user = mocks.create_logged_in_user()
        sut = HearThis(client_session_mock)

        # Act
        result = await sut.get_playlists(user)

        # Assert
        user = result[0].user
        self.assertIsNotNone(user.username)

    async def test_that_get_artist_tracks_returns_expected_data(self):
        # Arrange
        mock = AsyncMock()
        mock.get = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/myuserpermalink/",
            'get_artist_tracks_response.json',
            key="mykey",
            secret="mysecret",
            type="tracks",
            page="1",
            count="5"
        )
        user = mocks.create_logged_in_user()
        sut = HearThis(mock)

        # Act
        result = await sut.get_artist_tracks(user, "myuserpermalink")

        # Assert
        self.assertIsNotNone(result)
        feed = result[0]
        self.assertEqual(
            feed.title, "Shawne @ Back To The Roots 2 (05.07.2014)")
        self.assertIsNotNone(feed.user.username)
        self.assertEqual(feed.id, 48250)

    async def test_that_get_single_artist_returns_expected_data(self):
        # Arrange
        mock = AsyncMock()
        mock.get = mocks.RequestContextManagerMock.with_json_response(
            "https://api-v2.hearthis.at/myuserpermalink",
            'get_single_artist_response.json',
            )
        user = mocks.create_logged_in_user()
        sut = HearThis(mock)

        # Act
        result = await sut.get_single_artist(user, "myuserpermalink")

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.id, 100000)
