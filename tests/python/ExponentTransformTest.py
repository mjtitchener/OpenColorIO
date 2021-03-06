# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import unittest

import PyOpenColorIO as OCIO


class ExponentTransformTest(unittest.TestCase):
    TEST_ID = 'sample exponent'
    TEST_VALUES = [1, 2, 3, 4]
    TEST_NEGATIVE_STYLE = OCIO.NEGATIVE_MIRROR
    TEST_DIRECTION = OCIO.TRANSFORM_DIR_INVERSE

    def setUp(self):
        self.exp_tr = OCIO.ExponentTransform()

    def tearDown(self):
        self.exp_tr = None

    def test_transform_type(self):
        """
        Test the getTransformType() method.
        """
        self.assertEqual(self.exp_tr.getTransformType(), OCIO.TRANSFORM_TYPE_EXPONENT)

    def test_direction(self):
        """
        Test the setDirection() and getDirection() methods.
        """

        # Default initialized direction is forward.
        self.assertEqual(self.exp_tr.getDirection(),
                         OCIO.TRANSFORM_DIR_FORWARD)

        for direction in OCIO.TransformDirection.__members__.values():
            self.exp_tr.setDirection(direction)
            self.assertEqual(self.exp_tr.getDirection(), direction)

        # Wrong type tests.
        for invalid in (None, 1, 'test'):
            with self.assertRaises(TypeError):
                self.exp_tr.setDirection(invalid)

    def test_format_metadata(self):
        """
        Test the getFormatMetadata() method.
        """

        format_metadata = self.exp_tr.getFormatMetadata()
        format_metadata.setName(self.TEST_ID)
        self.assertIsInstance(format_metadata, OCIO.FormatMetadata)
        self.assertEqual(format_metadata.getName(), self.TEST_ID)
        format_metadata.setID(self.TEST_ID)
        self.assertEqual(format_metadata.getID(), self.TEST_ID)

    def test_negative_style(self):
        """
        Test the setNegativeStyle() and getNegativeStyle() methods.
        """

        # Default initialized negative style is clamp.
        self.assertEqual(self.exp_tr.getNegativeStyle(), OCIO.NEGATIVE_CLAMP)

        # Linear negative extrapolation is not valid for basic exponent style.
        for negative_style in OCIO.NegativeStyle.__members__.values():
            if negative_style != OCIO.NEGATIVE_LINEAR:
                self.exp_tr.setNegativeStyle(negative_style)
                self.assertEqual(
                    self.exp_tr.getNegativeStyle(), negative_style)
            else:
                with self.assertRaises(OCIO.Exception):
                    self.exp_tr.setNegativeStyle(negative_style)

    def test_values(self):
        """
        Test the setValue() and getValue() methods.
        """

        # Default initialized vars value is [1, 1, 1, 1]
        self.assertEqual(self.exp_tr.getValue(), [1, 1, 1, 1])

        self.exp_tr.setValue(self.TEST_VALUES)
        self.assertEqual(self.exp_tr.getValue(), self.TEST_VALUES)

        # Wrong type tests.
        for invalid in (None, 'hello', [1, 2, 3]):
            with self.assertRaises(TypeError):
                self.exp_tr.setValue(invalid)

    def test_validate(self):
        """
        Test the validate() method.
        """

        # Validate should pass with default values.
        self.exp_tr.validate()

        # Validate should pass with positive values.
        self.exp_tr.setValue([1, 2, 3, 4])
        self.exp_tr.validate()

        # Validate should fail with lower bound value of 0.01.
        self.exp_tr.setValue([-1, -2, -3, -4])
        with self.assertRaises(OCIO.Exception):
            self.exp_tr.validate()

        # Validate should fail with higher bound value of 100.
        self.exp_tr.setValue([101, 1, 1, 1])
        with self.assertRaises(OCIO.Exception):
            self.exp_tr.validate()

    def test_constructor_with_keyword(self):
        """
        Test ExponentTransform constructor with keywords and validate its values.
        """

        # With keywords in their proper order.
        exp_tr = OCIO.ExponentTransform(
            value=self.TEST_VALUES,
            negativeStyle=self.TEST_NEGATIVE_STYLE,
            direction=self.TEST_DIRECTION)

        self.assertEqual(exp_tr.getValue(), self.TEST_VALUES)
        self.assertEqual(exp_tr.getNegativeStyle(), self.TEST_NEGATIVE_STYLE)
        self.assertEqual(exp_tr.getDirection(), self.TEST_DIRECTION)

        # With keywords not in their proper order.
        exp_tr2 = OCIO.ExponentTransform(
            negativeStyle=self.TEST_NEGATIVE_STYLE,
            direction=self.TEST_DIRECTION,
            value=self.TEST_VALUES)

        self.assertEqual(exp_tr2.getValue(), self.TEST_VALUES)
        self.assertEqual(exp_tr2.getNegativeStyle(), self.TEST_NEGATIVE_STYLE)
        self.assertEqual(exp_tr2.getDirection(), self.TEST_DIRECTION)

    def test_constructor_with_positional(self):
        """
        Test ExponentTransform constructor without keywords and validate its values.
        """

        exp_tr = OCIO.ExponentTransform(
            self.TEST_VALUES,
            self.TEST_NEGATIVE_STYLE,
            self.TEST_DIRECTION)

        self.assertEqual(exp_tr.getValue(), self.TEST_VALUES)
        self.assertEqual(exp_tr.getNegativeStyle(), self.TEST_NEGATIVE_STYLE)
        self.assertEqual(exp_tr.getDirection(), self.TEST_DIRECTION)

    def test_constructor_wrong_parameter_type(self):
        """
        Test ExponentTransform constructor with a wrong parameter type.
        """

        for invalid in (None, 1):
            with self.assertRaises(TypeError):
                exp_tr = OCIO.ExponentTransform(invalid)
