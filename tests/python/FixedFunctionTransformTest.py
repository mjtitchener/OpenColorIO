# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import unittest

import PyOpenColorIO as OCIO


class FixedFunctionTransformTest(unittest.TestCase):
    TEST_STYLE = OCIO.FIXED_FUNCTION_ACES_GLOW_03
    TEST_PARAMS = [0, 1, 2]
    TEST_DIRECTION = OCIO.TRANSFORM_DIR_INVERSE

    def setUp(self):
        self.fixed_func_tr = OCIO.FixedFunctionTransform(OCIO.FIXED_FUNCTION_ACES_RED_MOD_03)

    def tearDown(self):
        self.fixed_func_tr = None

    def test_transform_type(self):
        """
        Test the getTransformType() method.
        """
        self.assertEqual(self.fixed_func_tr.getTransformType(), OCIO.TRANSFORM_TYPE_FIXED_FUNCTION)

    def test_direction(self):
        """
        Test the setDirection() and getDirection() methods.
        """

        # Default initialized direction is forward.
        self.assertEqual(self.fixed_func_tr.getDirection(),
                         OCIO.TRANSFORM_DIR_FORWARD)

        for direction in OCIO.TransformDirection.__members__.values():
            self.fixed_func_tr.setDirection(direction)
            self.assertEqual(self.fixed_func_tr.getDirection(), direction)

        # Wrong type tests.
        for invalid in (None, 1, 'test'):
            with self.assertRaises(TypeError):
                self.fixed_func_tr.setDirection(invalid)

    def test_format_metadata(self):
        """
        Test the getFormatMetadata() method.
        """

        format_metadata = self.fixed_func_tr.getFormatMetadata()
        self.assertIsInstance(format_metadata, OCIO.FormatMetadata)
        self.assertEqual(format_metadata.getElementName(), 'ROOT')
        self.assertEqual(format_metadata.getName(), '')
        self.assertEqual(format_metadata.getID(), '')
        format_metadata.setName('name')
        format_metadata.setID('id')
        self.assertEqual(format_metadata.getName(), 'name')
        self.assertEqual(format_metadata.getID(), 'id')

    def test_params(self):
        """
        Test the setParams() and getParams() methods.
        """

        # Default initialized params is an empty list.
        self.assertEqual(self.fixed_func_tr.getParams(), [])

        self.fixed_func_tr.setParams(self.TEST_PARAMS)
        self.assertEqual(self.fixed_func_tr.getParams(), self.TEST_PARAMS)

    def test_style(self):
        """
        Test the setStyle() and getStyle() methods.
        """

        # Default initialized style is red mod 3.
        self.assertEqual(self.fixed_func_tr.getStyle(),
                         OCIO.FIXED_FUNCTION_ACES_RED_MOD_03)

        for style in OCIO.FixedFunctionStyle.__members__.values():
            if style not in [OCIO.FIXED_FUNCTION_ACES_GAMUTMAP_02,
                             OCIO.FIXED_FUNCTION_ACES_GAMUTMAP_07,
                             OCIO.FIXED_FUNCTION_ACES_GAMUTMAP_13]:
                self.fixed_func_tr.setStyle(style)
                self.assertEqual(self.fixed_func_tr.getStyle(), style)

    def test_validate_direction(self):
        """
        Test the validate() method for direction.
        Direction must be forward or inverse.
        """

        self.fixed_func_tr.setDirection(OCIO.TRANSFORM_DIR_FORWARD)
        self.assertIsNone(self.fixed_func_tr.validate())

    def test_validate_params(self):
        """
        Test the validate() method for params.
        Initialization must have the correct number of params required for the style (possibly
        none).
        """

        self.fixed_func_tr = OCIO.FixedFunctionTransform(
            style=self.TEST_STYLE,
            direction=self.TEST_DIRECTION)

        self.assertIsNone(self.fixed_func_tr.validate())

        self.fixed_func_tr.setParams(self.TEST_PARAMS)
        with self.assertRaises(OCIO.Exception):
            self.fixed_func_tr.validate()

        self.fixed_func_tr.setStyle(OCIO.FIXED_FUNCTION_REC2100_SURROUND)
        self.fixed_func_tr.setParams([0.78])
        self.assertIsNone(self.fixed_func_tr.validate())

    def test_constructor_with_keywords(self):
        """
        Test FixedFunctionTransform constructor with keywords and validate its values.
        Initialization must have the correct number of params required for the style (possibly
        none).
        """

        fixed_func_tr = OCIO.FixedFunctionTransform(
            style=self.TEST_STYLE,
            params=[],
            direction=self.TEST_DIRECTION)

        self.assertEqual(fixed_func_tr.getStyle(), self.TEST_STYLE)
        self.assertEqual(fixed_func_tr.getParams(), [])
        self.assertEqual(fixed_func_tr.getDirection(), self.TEST_DIRECTION)

        # With keywords not in their proper order.
        fixed_func_tr2 = OCIO.FixedFunctionTransform(
            direction=self.TEST_DIRECTION,
            style=self.TEST_STYLE,
            params=[])

        self.assertEqual(fixed_func_tr2.getStyle(), self.TEST_STYLE)
        self.assertEqual(fixed_func_tr2.getParams(), [])
        self.assertEqual(fixed_func_tr2.getDirection(), self.TEST_DIRECTION)

        with self.assertRaises(OCIO.Exception):
            self.fixed_func_tr = OCIO.FixedFunctionTransform(
                style=self.TEST_STYLE,
                params=self.TEST_PARAMS,
                direction=self.TEST_DIRECTION)

        self.fixed_func_tr = OCIO.FixedFunctionTransform(
            style=OCIO.FIXED_FUNCTION_REC2100_SURROUND,
            params=[0.78])

        params = self.fixed_func_tr.getParams()
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0], 0.78)

        with self.assertRaises(OCIO.Exception):
            self.fixed_func_tr = OCIO.FixedFunctionTransform(
                style=OCIO.FIXED_FUNCTION_REC2100_SURROUND,
                params=[0.78, 0.42])

        with self.assertRaises(OCIO.Exception):
            self.fixed_func_tr = OCIO.FixedFunctionTransform(
                style=OCIO.FIXED_FUNCTION_REC2100_SURROUND)


    def test_constructor_with_positional(self):
        """
        Test FixedFunctionTransform constructor without keywords and validate its values.
        """

        fixed_func_tr = OCIO.FixedFunctionTransform(
            self.TEST_STYLE,
            [],
            self.TEST_DIRECTION)

        self.assertEqual(fixed_func_tr.getStyle(), self.TEST_STYLE)
        self.assertEqual(fixed_func_tr.getParams(), [])
        self.assertEqual(fixed_func_tr.getDirection(), self.TEST_DIRECTION)

    def test_constructor_wrong_parameter_type(self):
        """
        Test FixedFunctionTransform constructor with a wrong parameter type.
        """

        for invalid in (None, 1):
            with self.assertRaises(TypeError):
                fixed_func_tr = OCIO.FixedFunctionTransform(invalid)
