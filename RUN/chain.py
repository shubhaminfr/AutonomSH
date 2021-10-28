import os
import glob

path = os.getcwd()

solut_dir = path + '/SOLUT/'
currentSolut = path + '/currentSOLUT/'
temporal_dir = path + '/'

newest = max(glob.glob(solut_dir + '*.h5'), key = os.path.getctime)
print (newest)

#os.system('rm ' + currentSolut + '18Run_*')
os.system('cp ' + newest + ' ' + currentSolut + '.')
print 'Current Solut used : %s '%(newest)


print 'link %s with %s'%(currentSolut + 'linked.h5', newest)
os.system('ln -sf '+newest+' '+currentSolut + 'linked.h5')

num_tempo = os.popen('ls -d '+temporal_dir+'TEMPORAL* | wc -l').read()

num_tempo = str(int(num_tempo)+0)
print('TEMPORAL %s' %num_tempo)

os.mkdir(temporal_dir+'TEMPORAL'+num_tempo)
os.system('mv '+temporal_dir+'TEMPORALC/* '+temporal_dir+'TEMPORAL'+num_tempo)

os.system('mv avbp_log_* ./logfiles/.')
os.system('mv avbp_2020* ./logfiles/.')
os.system('mv chain_* ./chainfiles/.')

