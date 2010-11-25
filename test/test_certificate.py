#
# Copyright (c) 2010 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.
#

import time
from datetime import datetime, timedelta
import unittest

import M2Crypto

import certificate

from stubs import *

def yesterday():
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    now = datetime.now()
    then = now - timedelta(days=1)
    return then

class EntitlementCertificateTests(unittest.TestCase):

    def test_valid_order_date_gives_valid_cert(self):
        def getStubOrder():
            return StubOrder("2010-07-27T16:06:52Z",
                    "2011-07-26T20:00:00Z")

        cert = StubEntitlementCertificate(StubProduct('product'),
                start_date=datetime(2010, 7, 27),
                end_date=datetime(2050, 7, 26))

        self.assertTrue(cert.valid())

    def test_expired_order_date_gives_invalid_cert(self):
        def getStubOrder():
            return StubOrder("2010-07-27T16:06:52Z",
                    yesterday())

        cert = StubEntitlementCertificate(StubProduct('product'),
                start_date=datetime(2010, 7, 27),
                end_date=yesterday())

        self.assertFalse(cert.valid())

    def test_invalid_order_date_gives_valid_cert_with_grace(self):
        def getStubOrder():
            return StubOrder("2010-07-27T16:06:52Z",
                    yesterday())

        # order ends yesterday, but cert expires tomorrow
        cert = StubEntitlementCertificate(StubProduct('product'),
                start_date=datetime(2010, 7, 27),
                end_date=datetime.now() + timedelta(days=1),
                order_end_date=yesterday())

        self.assertTrue(cert.validWithGracePeriod())

    def test_invalid_x509_date_gives_invalid_cert_with_grace(self):
        def getStubOrder():
            return StubOrder("2010-07-27T16:06:52Z",
                    yesterday())

        # order ends yesterday, cert expires 5 minutes ago
        cert = StubEntitlementCertificate(StubProduct('product'),
                start_date=datetime(2010, 7, 27),
                end_date=datetime.now() - timedelta(minutes=5),
                order_end_date=yesterday())

        self.assertFalse(cert.validWithGracePeriod())
