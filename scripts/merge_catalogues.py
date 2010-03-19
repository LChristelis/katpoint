import numpy as np
import matplotlib.pyplot as plt

import katpoint

ant = katpoint.Antenna('KAT7, -30:43:17.34, 21:24:38.46, 1038, 12.0')
freq = 1800.0
freq_range = np.arange(900.0, 2100.0, 10.0)

old_all = katpoint.Catalogue(file('/var/kat/conf/source_list.csv'), antenna=ant, flux_freq_MHz=freq)
old = old_all.filter(flux_limit_Jy=10)
pks10 = katpoint.Catalogue(file('parkes_source_list.csv'), antenna=ant, flux_freq_MHz=freq)
pks = pks10.filter(flux_limit_Jy=10)
jy1_all = katpoint.Catalogue(file('kuehr1Jy_source_list.csv'), antenna=ant, flux_freq_MHz=freq)
jy1 = jy1_all.filter(flux_limit_Jy=10)

plt.figure(1)
plt.clf()

for n, src in enumerate(old):
    names = [src.name] + src.aliases
    print 'OLD:', names, ('%.1f Jy' % (src.flux_density(freq),)) if not np.isnan(src.flux_density(freq)) else ''
    print src.description
    plt.subplot(5, 6, n + 1)
    plt.plot(np.log10(freq_range), np.log10(src.flux_density(freq_range)), 'b')
    jy1_src, dist_deg = jy1.closest_to(src)
    if dist_deg < 3 / 60.:
        print ' --> 1JY:', [jy1_src.name] + jy1_src.aliases, \
              ('%.1f Jy' % (jy1_src.flux_density(freq),)) if not np.isnan(jy1_src.flux_density(freq)) else ''
        print '    ', jy1_src.description
        plt.plot(np.log10(freq_range), np.log10(jy1_src.flux_density(freq_range)), 'r')
        jy1.remove(jy1_src.name)
    pks_src, dist_deg = pks.closest_to(src)
    if dist_deg < 3 / 60.:
        print ' --> PKS:', [pks_src.name] + pks_src.aliases, \
              ('%.1f Jy' % (pks_src.flux_density(freq),)) if not np.isnan(pks_src.flux_density(freq)) else ''
        print '    ', pks_src.description
        plt.plot(np.log10(freq_range), np.log10(pks_src.flux_density(freq_range)), 'g')
        pks.remove(pks_src.name)
    plt.axis((np.log10(freq_range[0]), np.log10(freq_range[-1]), 0, 4))
    plt.xticks([]); plt.yticks([])
    print

plt.figtext(0.5, 0.93, 'Spectra (log S vs. log v) old=b, 1Jy=r, pks=g', ha='center', va='center')
