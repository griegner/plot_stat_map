from nilearn import plotting
from nilearn.plotting import cm
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
    stats_path = filedialog.askopenfilename(title='select stats image (NIFTI)')
    bg_path = filedialog.askopenfilename(title='select background image (NIFTI)')
    output_path = filedialog.asksaveasfilename(title='name output file')
    return stats_path, bg_path, output_path


def colorbar(vmin, vmax, output_file):
    print('colorbar: +/- %s to %s' % (vmin, vmax))
    cmap = cm.cold_hot
    norm = mpl.colors.Normalize(vmin=-vmax, vmax=vmax)
    maskedcolors = cmap(np.linspace(0, 1, 256))
    black = np.array([0, 0, 0, 1])
    maskedcolors[int(round(norm(-vmin) * 256)): int(round(norm(vmin) * 256)) + 1] = black
    maskedcmp = mpl.colors.ListedColormap(maskedcolors)
    fig, ax = plt.subplots(figsize=(.25, 8))
    mpl.colorbar.ColorbarBase(ax, cmap=maskedcmp, norm=norm, orientation='vertical', ticks=[])
    plt.savefig('%s_colorbar_%s-%s.png' % (output_file, vmin, vmax), dpi=300, transparent=True)


def save_img(min_slice, max_slice, stats_img, bg_img, vmin, vmax, slice, output_file):

    for i in range(min_slice, max_slice):
        print('slice: %s=%s' % (slice, i))
        plotting.plot_stat_map(stat_map_img=stats_img,
                               bg_img=bg_img,
                               threshold=vmin,
                               vmax=vmax,
                               display_mode=slice,
                               cut_coords=[i],
                               colorbar=False,
                               annotate=False,
                               draw_cross=False,
                               output_file='%s_%s=%s.png' % (output_file, slice, str(i)))


def main():

    while True:
        try:
            print('\nthresholded statistics')
            vmin = abs(float(input('vmin: ')))
            vmax = abs(float(input('vmax: ')))
            break
        except ValueError:
            print('try again...')

    stats_img, bg_img, output_file = browse_file()

    colorbar(vmin, vmax, output_file)

    save_img(-71, 72, stats_img, bg_img, vmin, vmax, 'x', output_file)
    save_img(-107, 74, stats_img, bg_img, vmin, vmax, 'y', output_file)
    save_img(-70, 82, stats_img, bg_img, vmin, vmax, 'z', output_file)

    print('done')


main()
