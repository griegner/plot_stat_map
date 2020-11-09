from nilearn import plotting
from nilearn.plotting import cm
from nilearn.image import math_img
from nilearn import datasets
import tkinter as tk
from tkinter import filedialog
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def browse_file():
    root = tk.Tk()
    root.withdraw()
    bg_path = filedialog.askopenfilename(title='select background image (NIFTI)')
    stats_path = filedialog.askopenfilename(title='select stats image (NIFTI)')
    output_path = filedialog.asksaveasfilename(title='name output file')
    return bg_path, stats_path, output_path


def colorbar(vmin, vmax, output_file):
    print(f'colorbar: +/- {vmin} to {vmax}')
    cmap = cm.cold_hot
    norm = mpl.colors.Normalize(vmin=-vmax, vmax=vmax)
    maskedcolors = cmap(np.linspace(0, 1, 256))
    black = np.array([0, 0, 0, 1])
    maskedcolors[int(round(norm(-vmin) * 256)): int(round(norm(vmin) * 256)) + 1] = black
    maskedcmp = mpl.colors.ListedColormap(maskedcolors)
    fig, ax = plt.subplots(figsize=(.25, 8))
    mpl.colorbar.ColorbarBase(ax, cmap=maskedcmp, norm=norm, orientation='vertical', ticks=[])
    plt.savefig(f'{output_file}_colorbar_{vmin}-{vmax}.png', dpi=300, transparent=True)


def save_img(min_slice, max_slice, bg_img, stats_img, vmin, vmax, slice, output_file):

    for i in range(min_slice, max_slice):
        print('slice: %s=%s' % (slice, i))
        img = plotting.plot_stat_map(bg_img=bg_img,
                               stat_map_img=stats_img,
                               threshold=vmin,
                               vmax=vmax,
                               display_mode=slice,
                               cut_coords=[i],
                               colorbar=False,
                               annotate=False,
                               draw_cross=False)
        img.savefig(f'{output_file}_{slice}={i}.png', dpi=300)
	img.close()


def main():

    while True:
        try:
            print('\nset thresholding')
            vmin = abs(float(input('vmin: ')))
            vmax = abs(float(input('vmax: ')))
            mask = input('mask stats img y/n: ')
            break
        except ValueError:
            print('try again...')

    bg_img, stats_img, output_file = browse_file()

    if mask == 'y':
        brain_mask = datasets.load_mni152_brain_mask()
        stats_img = math_img('img1 * img2', img1=stats_img, img2=brain_mask)

    colorbar(vmin, vmax, output_file)

    save_img(-71, 72, bg_img, stats_img, vmin, vmax, 'x', output_file)
    save_img(-107, 74, bg_img, stats_img, vmin, vmax, 'y', output_file)
    save_img(-70, 82, bg_img, stats_img, vmin, vmax, 'z', output_file)

    print('done')


main()
