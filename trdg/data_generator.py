import random as rnd

import numpy as np
import cv2

from trdg import computer_text_generator, background_generator, distorsion_generator

try:
    from trdg import handwritten_text_generator
except ImportError as e:
    print("Missing modules for handwritten text generation.")


class FakeTextDataGenerator(object):
    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """

        return cls.generate(*t)

    @classmethod
    def generate(
        cls,
        text,
        font,
        size,
        skewing_angle,
        random_skew,
        blur,
        random_blur,
        background_type,
        distorsion_type,
        distorsion_orientation,
        width,
        alignment,
        text_color,
        orientation,
        space_width,
        character_spacing,
        margins,
        fit,
        word_split,
        image_path,
    ):

        margin_top, margin_left, margin_bottom, margin_right = margins
        horizontal_margin = margin_left + margin_right
        vertical_margin = margin_top + margin_bottom

        ##########################
        # Create picture of text #
        ##########################

        image = computer_text_generator.generate(
            text,
            font,
            text_color,
            size,
            orientation,
            space_width,
            character_spacing,
            fit,
            word_split,
        )

        image = np.array(image)[:, :, ::-1]
        image_height, image_width, image_channel = image.shape

        random_angle = rnd.randint(0 - skewing_angle, skewing_angle)
        rotate_matrix = cv2.getRotationMatrix2D((image_width / 2, image_height / 2), random_angle, 1)
        rotated_img = cv2.warpAffine(image, rotate_matrix, (image_width, image_height))

        #############################
        # Apply distorsion to image #
        #############################
        if distorsion_type == 0:
            distorted_img = rotated_img  # Mind = blown
        # TODO - remove mask parameter
        #elif distorsion_type == 1:
        #    distorted_img, distorted_mask = distorsion_generator.sin(
        #        rotated_img,
        #        vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
        #        horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
        #    )
        #elif distorsion_type == 2:
        #    distorted_img, distorted_mask = distorsion_generator.cos(
        #        rotated_img,
        #        vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
        #        horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
        #    )
        #else:
        #    distorted_img, distorted_mask = distorsion_generator.random(
        #        rotated_img,
        #        vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
        #        horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
        #    )

        ##################################
        # Resize image to desired format #
        ##################################

        # Horizontal text
        if orientation == 0:
            new_width = int(
                distorted_img.shape[1]
                * (float(size - vertical_margin) / float(distorted_img.shape[0]))
            )
            resized_img = cv2.resize(distorted_img, (new_width, size - vertical_margin), interpolation=cv2.INTER_AREA)
            background_width = width if width > 0 else new_width + horizontal_margin
            background_height = size
        # Vertical text
        elif orientation == 1:
            new_height = int(
                float(distorted_img.shape[0])
                * (float(size - horizontal_margin) / float(distorted_img.shape[1]))
            )
            resized_img = cv2.resize(distorted_img,  (size - horizontal_margin, new_height), interpolation=cv2.INTER_AREA)
            background_width = size
            background_height = new_height + vertical_margin
        else:
            raise ValueError("Invalid orientation")

        #############################
        # Generate background image #
        #############################
        if background_type == 0:
            background_img = background_generator.gaussian_noise(
                background_height, background_width
            )
        elif background_type == 1:
            background_img = background_generator.plain_white(
                background_height, background_width
            )
        # TODO
        #elif background_type == 2:
        #    background_img = background_generator.quasicrystal(
        #        background_height, background_width
        #    )
        else:
            background_img = background_generator.image(
                background_height, background_width, image_path
            )

        #############################
        # Place text with alignment #
        #############################

        new_text_height, new_text_width = resized_img.shape[:2]
        if alignment == 0 or width == -1:
            background_img[margin_top: margin_top + new_text_height, margin_left: margin_left + new_text_width, :] = resized_img
        elif alignment == 1:
            left_from = int(background_width / 2 - new_text_width / 2)
            background_img[margin_top: margin_top + new_text_height, left_from: left_from + new_text_width] = resized_img
        else:
            left_from = background_width - new_text_width - margin_right
            background_img[margin_top: margin_top + new_text_height, left_from: left_from + new_text_width] = resized_img

        ##################################
        # Apply gaussian blur #
        ##################################
        radius = blur if not random_blur else rnd.randint(0, blur)
        if radius % 2 == 0:
            radius -= 1
        if radius == -1:
            final_image = background_img
        else:
            final_image = cv2.GaussianBlur(background_img, (radius, radius), 0)

        return final_image, text

