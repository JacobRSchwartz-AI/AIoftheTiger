# Method to preprocess a folder of images by creating a CSV with the index
# of images we want to include in our dataset as the results of their similarity score
def image_preprocessor(folder, start_prop):
    time.sleep(start_prop)
    f = open("directory.txt", "r")
    path = f.read()
    img_folder = path + "CSV\\\\" + folder

    # Define the path that will contain the CSV of indices of the images that
    # are different based on their similarity score
    # csv_path = img_folder[:-7] + "CSV.csv"
    # print(csv_path)
    dst = path + "Data\\\\Unscored Data\\\\" + folder

            # print("Already exists ")
    img_folder = os.listdir(dst)
    img_folder = sorted_alphanumeric(img_folder)

    starting_frame = math.floor(start_prop*len(img_folder))
    ending_frame = math.floor((start_prop+0.1)*len(img_folder))

    # Loop counter
    image = starting_frame
    sim_score = 0
    sim_score_max = [0, 0]
    # Always shows the first image
    images_to_show = [starting_frame]

    # Define which images to score
    # print("Preprocessing images ")
    while image < ending_frame:
        file_path = dst + "\\" + img_folder[image]
        img_1 = cv2.imread(file_path)
        # Picks an image as a starting point, checks the next 50 images
        for x in range(1, 51):
            if image + x < ending_frame:
                file_path_2 = dst + "\\" + img_folder[image + x]
                img_2 = cv2.imread(file_path_2)
                sim_score = similarity_Score(img_1, img_2)
                # Keeps only the index of the image that is the most different from the first image
                if sim_score >= sim_score_max[0]:
                    sim_score_max[0] = sim_score
                    sim_score_max[1] = image + x
            # Makes sure we keep the last image, signals that we are done
            else:
                return images_to_show
        # Pulls the index of the most dissimilar images.
        # Continues the loop with that image as the base and checking the next 50 against it.
        image = sim_score_max[1]
        images_to_show.append(image)
        print(str(sim_score_max[1]) + " out of " + str(len(img_folder) - 1) + " complete")
        sim_score_max = [0, 0]

    # write_to_file(csv_path, images_to_show)
    # shutil.rmtree(dst)


# determines similarity score between two images
def similarity_Score(image1, image2):
    error = 0
    normalizer = len(image1) * len(image1[0]) * len(image1[0][0])
    image1_array = np.asarray(image1) / 255
    image2_array = np.asarray(image2) / 255
    score_array = image1_array - image2_array
    score_array = np.square(score_array)
    error = 100 * score_array.sum() / normalizer
    return error