import sox
import sys
import os

GAP_BETWEEN_EACH_USONIC_IN_MS=500
USONIC_OUTPUT_FILE_NAME="usonic_output.wav"
SILENCE_ADDED_WAV="usonic_with_silence.wav"
FINAL_OUTPUT_WAV="output.wav"

def prepare_usonic_file(usonic_file_path, usoniclen_in_sec, soniclen_in_sec):

    no_of_loops = (int)(soniclen_in_sec*1000/(usoniclen_in_sec*1000 + GAP_BETWEEN_EACH_USONIC_IN_MS))

    tfm = sox.Transformer()
    tfm.pad(0, GAP_BETWEEN_EACH_USONIC_IN_MS/1000)
    tfm.build_file(input_filepath=usonic_file_path, output_filepath=SILENCE_ADDED_WAV)

    comb = sox.Combiner()
    combine_list = []
    for i in range(no_of_loops):
        combine_list.append(SILENCE_ADDED_WAV)

    ret = comb.build(combine_list, USONIC_OUTPUT_FILE_NAME, combine_type="concatenate")
    if ret == False:
        print(f'Combine failed for USonic')
    
    return ret


def get_file_length(file_path):
    return sox.file_info.duration(file_path)

def get_no_of_channels(file_path):
    return sox.file_info.channels(file_path)

if __name__ == '__main__':  
    input_args = sys.argv

    usonic_file = input_args[1]
    sonic_file = input_args[2]

    usonic_len = get_file_length(usonic_file)
    sonic_len = get_file_length(sonic_file)

    if get_no_of_channels(sonic_file) == 2:
        print(f'Channel count is 2')
        tfm = sox.Transformer()
        tfm.convert(n_channels=1)
        tfm.build_file(input_filepath=sonic_file, output_filepath=sonic_file)
    
    prepare_usonic_file(usonic_file, usonic_len, sonic_len)

    merge_list = [sonic_file, USONIC_OUTPUT_FILE_NAME]
    comb = sox.Combiner()

    ret = comb.build(merge_list, FINAL_OUTPUT_WAV, combine_type="mix")

    if ret == False:
        print(f'Merge failed')

    print(f'Merge Successful')

    os.remove(USONIC_OUTPUT_FILE_NAME)
    os.remove(SILENCE_ADDED_WAV)