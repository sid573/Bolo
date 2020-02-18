from __future__ import print_function
import sounddevice as sd
from scipy.io.wavfile import write
import parselmouth
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dtw import dtw
import base64
import io 
import json




# gender = input("Press M for Male , F for Female: ")
# gender = gender.upper()

print("Enter number corresponding to sentence:\n"
      "1) Can I Have Some Kheer ?\n"
      "2) I Am Visiting Him Next Month\n"
      "3) I Love Dosas\n"
      "4) I Want To See A Rainbow\n"
      "5) My Mom Cooked Brinjal For Lunch\n"
      "6) This Is My Favorite Shirt\n")
# choice=input()

file = [
     "CanIHaveSomeKheer",
    "IAmVisitingHimNextMonth",
     "ILoveDosas",
    "IWantToSeeARainbow",
    "MyMomCookedBrinjalForLunch",
    "ThisIsMyFavoriteShirt"
]

rec_time=[2,3,2,3,3,3]

def record(filename,time):
    print("Recording for ",time,"Seconds")
    input("Press Enter to Record...")
    fs = 44100  # Sample rate
    myrecording = sd.rec(int(time * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    print("Recording done")
    write(filename, fs, myrecording)  # Save as WAV file

def draw_intensity(intensity):
    cur = intensity.values.T          # / np.mean(intensity.values.T)
    plt.plot(intensity.xs(), cur, linewidth=3, color='w')
    plt.plot(intensity.xs(), cur, linewidth=1)
    plt.grid(False)
    plt.ylim(0)
    plt.ylabel("intensity [dB]")

def draw_pitch(pitch):
    # Extract selected pitch contour, and
    # replace unvoiced samples by NaN to not plotpip install py2exe
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan
    # plt.plot(pitch.xs(), pitch_values, linewidth=3, color='w')
    plt.plot(pitch.xs(), pitch_values, linewidth=3, )
    plt.grid(False)
    plt.axis('off')
    # plt.ylim(0, pitch.ceiling)
    # plt.ylabel("fundamental frequency [Hz]")


def bolo_host(gender,choice,filename):
    sns.set()
    plt.rcParams['figure.dpi'] = 100
    gender = gender.upper()

    referfile="./AudioClips/"+gender+"_"+file[int(choice)-1]+".wav"
    testfile=filename

    # record(testfile,rec_time[int(choice)-1])

    test_parsel = parselmouth.Sound(testfile)
    refer_parcel = parselmouth.Sound(referfile)

    test_intensity = test_parsel.to_intensity()
    refer_intensity = refer_parcel.to_intensity()

    test_pitch = test_parsel.to_pitch()
    refer_pitch = refer_parcel.to_pitch()

    # plt.figure()
    # draw_intensity(test_intensity)
    # draw_intensity(refer_intensity)
    # plt.xlim([test_parsel.xmin, test_parsel.xmax])
    # plt.suptitle('Intensity', fontsize=16)

    plt.figure()
    draw_pitch(test_pitch)
    # draw_pitch(refer_pitch)
    plt.xlim([test_parsel.xmin, test_parsel.xmax])
    # plt.suptitle('Pitch', fontsize=16)


    refer_intensity_norm =refer_intensity.values.T /np.mean (refer_intensity.values.T)
    test_intensity_norm =test_intensity.values.T /np.mean (test_intensity.values.T)
    euclidean_norm = lambda x, y: np.abs(x - y)

    d_intensity, cost_matrix, acc_cost_matrix, path_intensity = dtw(test_intensity_norm, refer_intensity_norm, dist=euclidean_norm)

    refer_pitch_norm =refer_pitch.selected_array['frequency'] /np.mean (refer_pitch.selected_array['frequency'])
    test_pitch_norm =test_pitch.selected_array['frequency'] /np.mean (test_pitch.selected_array['frequency'])

    d_pitch, cost_matrix, acc_cost_matrix, path_pitch = dtw(test_pitch_norm, refer_pitch_norm, dist=euclidean_norm)


    test_intensity_post= np.zeros(path_intensity[0].size)
    j=0
    for i in path_intensity[0] :
        test_intensity_post[j] =test_intensity_norm[i]
        j=j+1

    refer_intensity_post= np.zeros(path_intensity[1].size)
    j=0
    for i in path_intensity[1] :
        refer_intensity_post[j] =refer_intensity_norm[i]
        j=j+1

    diff_intensity_post=0
    for i in range(path_intensity[0].size):
        diff_intensity_post = diff_intensity_post+euclidean_norm(refer_intensity_post[i],test_intensity_post[i])





    test_pitch_post= np.zeros(path_pitch[0].size)
    j=0
    for i in path_pitch[0] :
        test_pitch_post[j] =test_pitch_norm[i]
        j=j+1

    refer_pitch_post= np.zeros(path_pitch[1].size)
    j=0
    for i in path_pitch[1] :
        refer_pitch_post[j] =refer_pitch_norm[i]
        j=j+1

    diff_pitch_post=0
    for i in range(path_pitch[0].size):
        diff_pitch_post = diff_pitch_post+euclidean_norm(refer_pitch_post[i],test_pitch_post[i])


    print("Pitch DTW: ",d_pitch)
    print("Pitch diff: ",diff_pitch_post)
    print("Intensity DTW: ",d_intensity)
    print("Intensity diff: ",diff_intensity_post)
    # print("Time diff ",sum(path_intensity[0])-sum(path_intensity[1]))


    # plt.show()
    pic_IObytes = io.BytesIO()
    plt.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    pic_hash = base64.b64encode(pic_IObytes.read())
    dic = {}
    dic['image'] = str(pic_hash)
    dic['pitch'] = diff_pitch_post
    dic['intensity'] = diff_intensity_post
    # print(dic)
    # print (json.dumps(dic))
    return json.dumps(dic)
