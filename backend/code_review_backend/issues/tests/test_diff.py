# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import hashlib

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from code_review_backend.issues.models import Diff
from code_review_backend.issues.models import Repository


class DiffAPITestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(username="crash_user")

        # Create a repo
        self.repo = Repository.objects.create(
            id=1, phid="PHID-REPO-xxx", slug="myrepo", url="http://repo.test/myrepo"
        )

        # Create a stack with 2 revisions & 3 diffs
        for i in range(2):
            self.repo.revisions.create(
                id=i + 1,
                phid=f"PHID-DREV-{i+1}",
                title=f"Revision {i+1}",
                bugzilla_id=10000 + i,
            )
        for i in range(3):
            Diff.objects.create(
                id=i + 1,
                phid=f"PHID-DIFF-{i+1}",
                revision_id=(i % 2) + 1,
                review_task_id=f"task-{i}",
                mercurial_hash=hashlib.sha1(f"hg {i}".encode("utf-8")).hexdigest(),
            )

    def test_list_diffs(self):
        """
        Check we can list all diffs with their revision
        """
        response = self.client.get("/v1/diff/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                "count": 3,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "revision": {
                            "id": 1,
                            "repository": "myrepo",
                            "phid": "PHID-DREV-1",
                            "title": "Revision 1",
                            "bugzilla_id": 10000,
                            "diffs_url": "http://testserver/v1/revision/1/diffs/",
                            "phabricator_url": "https://phabricator.services.mozilla.com/D1",
                        },
                        "phid": "PHID-DIFF-1",
                        "review_task_id": "task-0",
                        "mercurial_hash": "a2ac78b7d12d6e55b9b15c1c2048a16c58c6c803",
                        "issues_url": "http://testserver/v1/diff/1/issues/",
                        "nb_issues": 0,
                    },
                    {
                        "id": 2,
                        "revision": {
                            "id": 2,
                            "repository": "myrepo",
                            "phid": "PHID-DREV-2",
                            "title": "Revision 2",
                            "bugzilla_id": 10001,
                            "diffs_url": "http://testserver/v1/revision/2/diffs/",
                            "phabricator_url": "https://phabricator.services.mozilla.com/D2",
                        },
                        "phid": "PHID-DIFF-2",
                        "review_task_id": "task-1",
                        "mercurial_hash": "32d2a594cfef74fcb524028d1521d0d4bd98bd35",
                        "issues_url": "http://testserver/v1/diff/2/issues/",
                        "nb_issues": 0,
                    },
                    {
                        "id": 3,
                        "revision": {
                            "id": 1,
                            "repository": "myrepo",
                            "phid": "PHID-DREV-1",
                            "title": "Revision 1",
                            "bugzilla_id": 10000,
                            "diffs_url": "http://testserver/v1/revision/1/diffs/",
                            "phabricator_url": "https://phabricator.services.mozilla.com/D1",
                        },
                        "phid": "PHID-DIFF-3",
                        "review_task_id": "task-2",
                        "mercurial_hash": "30b501affc4d3b9c670fc297ab903b406afd5f04",
                        "issues_url": "http://testserver/v1/diff/3/issues/",
                        "nb_issues": 0,
                    },
                ],
            },
        )
