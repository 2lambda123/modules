import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import abundance_matching as am
from PlotParams import *
import DwarfMethods as dm
import RadialDependence as rd


StellarMasses = 10**6*np.array([0.14,0.54,0.77,0.82,1.3,1.4,1.6,2.1,2.7,3.5,3.5,4.5,6.0,6.4,6.6,7.8,8.3,16,16,17,19,37,44,47,51,52,62,76,100,100,190,270])
#luminosity = 10**np.linspace(4,9,16)
#halo_masses = 10**np.linspace(9,11.5,20)
ML_ratio = 1 #mass to luminosity ratio from Brook 2014 was 1.6. 
min_lum = 10**3





def convert_Mvir(Mvir, model):
    if isinstance(model, am.Moster) or isinstance(model, am.Sawala):
        return dm.convert_Mhalo_z0(Mvir, 200)
    if isinstance(model, am.GarrisonKimmel16) or isinstance(model, am.GarrisonKimmel) or isinstance(model, am.Behroozi):
        return Mvir
    if isinstance(model, am.Brook):
        return dm.convert_Mhalo_z0(Mvir, 350)



def plot_ngreater(min_lum=10**3,ls='-',mstar_axes=True):
    stellar_masses = 10**np.linspace(5,9,25)
    halo_masses = 10**np.linspace(9,11.5,20)
    #for model in [am.Moster(), am.GarrisonKimmel(), am.Brook(), am.GarrisonKimmel16(), am.Sawala(), am.Behroozi()]:

    for model in [am.Sawala(), am.Moster(reionization=True), am.GarrisonKimmel(reionization=True), am.Brook(reionization=True), am.GarrisonKimmel16(reionization=True), am.Behroozi(reionization=True)]:
        print model.label, 'on this model'
        if mstar_axes:
            halo_masses = model.stellar_to_halo_mass(stellar_masses)
            N_visible,_ = model.ngreater(halo_masses,min_lum)
            plt.plot(stellar_masses, N_visible,label=model.label,color=model.color,linestyle=model.ls,lw=linewidth)
        else:
            N_visible,_ = model.ngreater(halo_masses,min_lum)
            plt.plot(halo_masses, N_visible,label=model.label,color=model.color,linestyle=ls,lw=linewidth)

    plt.ylabel('$N_{halos} > 10^%d$ [$M_\odot$]' %np.log10(min_lum),fontsize=label_font)
    plt.xscale('log')
    #plt.yscale('log')
    plt.ylim((0,14))
    plt.legend(loc='upper left',frameon=False,fontsize=legend_size)
    plt.tick_params(axis='both', which='major', labelsize=tick_size)
    plt.gcf().subplots_adjust(bottom=0.15)
    
    plt.vlines(StellarMasses[-5:], plt.ylim()[0], plt.ylim()[1], linestyles='--',color='black')

    if mstar_axes:
        plt.xlabel('$M_* \ \mathrm{of \ Host} \ \mathrm{[M_\odot]}$',fontsize=label_font)
        plt.xlim((stellar_masses[0],stellar_masses[-1]))
        plt.savefig('Ngreater_%d' %np.log10(min_lum))
    else:
        plt.xlabel('Mass of Host [$M_\odot$]',fontsize=label_font)
        plt.xlim((halo_masses[0],halo_masses[-1]))
        plt.savefig('Ngreater_vs_mhalo_%d' %np.log10(min_lum))
    plt.close()



def plot_P_at_least_one(min_lum=10**3,ls='-',mstar_axes=True):
    stellar_masses = 10**np.linspace(5,9,25)
    halo_masses = 10**np.linspace(9,11.5,20)    
    #for model in [am.Moster(), am.GarrisonKimmel(), am.Brook(), am.GarrisonKimmel16(), am.Sawala(), am.Behroozi()]:
    for model in [am.Sawala(), am.Moster(reionization=True), am.GarrisonKimmel(reionization=True), am.Brook(reionization=True), am.GarrisonKimmel16(reionization=True)]:

        print model.label, 'on this model'
        if mstar_axes:
            halo_masses = model.stellar_to_halo_mass(stellar_masses)
            Pgt1 = model.P_at_least_one(halo_masses,min_lum)
            plt.plot(stellar_masses, Pgt1,label=model.label,color=model.color,linestyle=model.ls,lw=linewidth)
        else:
            Pgt1 = model.P_at_least_one(halo_masses,min_lum)
            plt.plot(halo_masses, Pgt1,label=model.label,color=model.color,linestyle=model.ls,lw=linewidth)

    plt.ylabel('$\mathrm{P}(\geq 1 \mathrm{halo})$',fontsize=label_font)
    plt.xscale('log')
    #plt.yscale('log')
    plt.ylim((0,1))
    plt.legend(loc='upper left',frameon=False,fontsize=legend_size)
    plt.tick_params(axis='both', which='major', labelsize=tick_size)
    plt.gcf().subplots_adjust(bottom=0.15)

    plt.vlines(StellarMasses[-5:], plt.ylim()[0], plt.ylim()[1], linestyles='--',color='black')

    if mstar_axes:
        plt.xlabel('$M_* \ \mathrm{of \ Host} \ [\mathrm{M_\odot}]$',fontsize=label_font)    
        plt.xlim((stellar_masses[0],stellar_masses[-1]))
        plt.savefig('ProbabilityOfOne_%d' %np.log10(min_lum))
    else:
        plt.xlabel('Mass of Host [$\mathrm{M_\odot}$]',fontsize=label_font)
        plt.xlim((halo_masses[0],halo_masses[-1]))
        plt.savefig('ProbabilityOfOne_vs_mhalo_%d' %np.log10(min_lum))
    plt.close()
        


def plotMoster():
    M = 10**np.arange(7.5,12.5,.25)
    model =  am.Moster()
    for a in [1.0,0.6,0.3]:
        mstar = model.getStellarMass(M,a)
        #print mstar, model_label
        plt.plot(M, mstar, label=str(a),lw=linewidth)

    plt.legend(loc='lower right',fontsize=legend_size,frameon=False)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('$M_{halo} \mathrm{[M_\odot]}$',fontsize=label_font)
    plt.ylabel('$M_* \mathrm{[M_\odot]}$',fontsize=label_font)
    plt.ylim((10**3,10**11))
    plt.xlim((10**7.5,10**12.5))
    plt.tick_params(axis='both', which='major', labelsize=tick_size)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.savefig('moster_smhm_relation') # compare to figure 5 in paper
    plt.close()
    

def plotMstar_v_Mhalo():
    a = 1.0
    M = 10**np.arange(7.5,12.5,.25)
    AMmodels=[am.Moster(), am.Behroozi(), am.GarrisonKimmel(), am.Brook(), am.GarrisonKimmel16(), am.Sawala(), am.GK16_grow()]
    for model in AMmodels:
        mstar = model.getStellarMass(M,a)
        #print mstar, model_label
        plt.plot(M, mstar, label=model.label,lw=linewidth, color=model.color)
        if isinstance(model, am.GarrisonKimmel16) or isinstance(model, am.Sawala) or isinstance(model, am.GK16_grow):
            mstar_up = model.getStellarMass_up1sig(M,a)
            mstar_down = model.getStellarMass_down1sig(M,a)
            plt.fill_between(M,mstar_up,mstar_down, facecolor=model.color, alpha=0.2)
            #mstar_rand = model.getStellarMass_random(M,a)
            #plt.scatter(M,mstar_rand,color=model.color)
            

    plt.legend(loc='lower right',fontsize=legend_size,frameon=False)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('$M_{halo} \mathrm{[M_\odot]}$',fontsize=label_font)
    plt.ylabel('$M_* \mathrm{[M_\odot]}$',fontsize=label_font)
    plt.ylim((10**3,10**11))
    plt.xlim((10**7.5,10**12.5))
    plt.tick_params(axis='both', which='major', labelsize=tick_size)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.savefig('smhm_relation') # compare to figure 5 in paper
    plt.close()


def plotBentbyBaryons():
    #f,ax = plt.subplots(ncols=1)
    a = 1.0
    M = 10**np.arange(7.5,np.log10(5e10),.15)
    AMmodels= [am.Moster(), am.Sawala()]
    model_labels = ['Moster','Sawala']
    colors = ['blue','red']
    for model,model_label,color in zip(AMmodels,model_labels,colors):
        mstar = model.getStellarMass(M,a)
        #print mstar, model_label
        plt.plot(M, mstar, label=model_label,linewidth=5, color=color)

    plt.legend(loc='lower right',frameon=False,fontsize=26)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('$M_{halo} \mathrm{[M_\odot]}$',fontsize=30)
    plt.ylabel('$M_* \mathrm{[M_\odot]}$',fontsize=30)
    plt.ylim((10**3,10**8))
    plt.xlim((10**8,5e10))
    plt.tick_params(axis='both', which='major', labelsize=21)
    #plt.gca().tight_layout()	
    plt.gcf().subplots_adjust(bottom=0.17)
    plt.gcf().subplots_adjust(left=0.17)
    plt.savefig('BentByBaryons') # compare to figure 4 in bent by baryons
    plt.close()

# New plot to highlight dependence on min_lum
# x-axis: min lum. 10**3 - 10**5
# y-axis: number of halos greater than that luminosity. 
# pick a host halo mass of around IC1613. 10**10? 10**11?
# plot one panel with all the models as their own line
# plot another panel with the mass of the host changing?


# above GK16 completeness limit, 4.5*10^5 Mstar there are 11 in real MW including LMC, SMC. this is for 300 kpc
# above 10**6, there are 7 satellites.
# they use 1.6e12 Msun host halo mass
# compare to figure 3 of the elvis paper. what is going on???? Why so bad????
# I would get a grey band at 20, not at 10.





# I am greatly overpredicting the number of satellites above 10**6 in my mock MW.
# Isn't this a big problem!!!!

def ngreater_v_minlum(mw=False, reion=False, fixdmhalo=False):
    min_lums = 10**np.linspace(3,7,25)
    for model in [am.Moster(hostSHMF=mw,reionization=True), am.GarrisonKimmel(hostSHMF=mw,reionization=True),  am.GarrisonKimmel16(hostSHMF=mw,reionization=True), am.Brook(hostSHMF=mw,reionization=True), am.Sawala(hostSHMF=mw), am.Moster(hostSHMF=mw), am.GarrisonKimmel(hostSHMF=mw), am.Brook(hostSHMF=mw), am.GarrisonKimmel16(hostSHMF=mw)]:
    #for model in [am.GarrisonKimmel(hostSHMF=mw,reionization=True), am.GarrisonKimmel(hostSHMF=mw)]:

    #for model in [am.Moster(hostSHMF=mw,reionization=reion), am.GarrisonKimmel(hostSHMF=mw,reionization=reion), am.Brook(hostSHMF=mw,reionization=reion), am.GarrisonKimmel16(hostSHMF=mw,reionization=reion), am.Sawala(hostSHMF=mw)]:
        if mw:
            #halo_mass = 1.6*10**12  # this is B&N def. need to convert to M350 for brook, and M200 for moster
            halo_mass = 1.2*10**12  # this is B&N def. need to convert to M350 for brook, and M200 for moster
            G = 4.157e-39  # kpc^3/Msun/s^2
            H = dm.Hubble(a=1) # in 1/s
            rho_crit = (3*H**2)/(8*np.pi*G) # in Msun/kpc^3
            rvir = (halo_mass*3/(4*np.pi*103.86*rho_crit))**(1/3.) # in kpc
            r_ratio = 300/rvir
            print r_ratio, 'ratio of r=300 to rvir'

            halo_mass = convert_Mvir(halo_mass,model)
            # this gives me the number of satellites within Rvir of that host, where rvir is the B&N definition.
        else:
            if fixdmhalo:
                tmpmodel=am.Moster()
                halo_mass = tmpmodel.stellar_to_halo_mass(270*10**6 ,a=1.0)
                halo_mass = convert_Mvir(halo_mass,model)
            else:
                halo_mass = model.stellar_to_halo_mass(270*10**6 ,a=1.0) #halo_mass = 10**10.75 biggest field 
        print model.label, 'on this model'
        N_visible = np.array([model.ngreater(halo_mass,minlum)[0] for minlum in min_lums])
        if mw:
            N_visible = N_visible* rd.getK(r_ratio)
            print rd.getK(r_ratio), 'multiplicative factor of r/rvir'
            

        plt.plot(min_lums, N_visible,label=model.label,color=model.color,lw=linewidth,ls=model.ls)
        if mw:  # how many satellites above GK16 completeness limit? there are 11 in real MW including LMC, SMC
            print model.ngreater(halo_mass,4.5*10**5 / ML_ratio)[0], model.label, 'above completeness limit'
            print model.ngreater(halo_mass,10**6)[0], model.label, 'above 10**6'
            print model.ngreater(halo_mass,10**3)[0], model.label, 'above 10**3'
    

    plt.ylabel('$N_{halos} > M_*^{\mathrm{min}}$',fontsize=label_font)
    plt.xscale('log')
    #plt.yscale('log')
    #plt.ylim((0,8))
    plt.legend(loc='upper right',frameon=False,fontsize=legend_size)
    plt.tick_params(axis='both', which='major', labelsize=tick_size)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.xlabel('$M_*^{\mathrm{min}} \, [\mathrm{M_\odot}]$', fontsize=label_font)
    plt.xlim((min_lums[0],min_lums[-1]))

    extra=''
    if reion:
        extra+='reionization'
    if fixdmhalo:
        extra+='fixed_dm_mass'

    if mw:
        #plt.vlines(4.5*10**5/ML_ratio,0,100)
        plt.savefig('Ngreater_vs_minlum_MWsize')
    else:
        plt.savefig('Ngreater_vs_minlum'+extra)
    plt.close()

#ngreater_v_minlum(mw=False,reion=False,fixdmhalo=True)
#ngreater_v_minlum(mw=False,reion=True,fixdmhalo=False)
ngreater_v_minlum(mw=True)



#plotMoster()
#plot_ngreater(10**3,mstar_axes=True)
#plot_ngreater(10**4,mstar_axes=True)
#plot_ngreater(10**5,mstar_axes=True)

#plot_ngreater(10**3,mstar_axes=False)
#plot_ngreater(10**4,mstar_axes=False)



#plot_P_at_least_one(min_lum=10**4,mstar_axes=False)
#plot_P_at_least_one(min_lum=10**3,mstar_axes=False)

#plot_P_at_least_one(min_lum=10**3,mstar_axes=True)
#plot_P_at_least_one(min_lum=10**4,mstar_axes=True)
#plot_P_at_least_one(min_lum=10**5,mstar_axes=True)


"""
am.halo_to_stellar_mass(np.array([10**10,10**10.5]),model='moster')
halo_masses = am.stellar_to_halo_mass(luminosity,model='moster')

plt.plot(luminosity, halo_masses)
plt.xlabel('Luminosity [$L_\odot$]')
plt.ylabel('DM Halo Mass [$M_\odot$]')
plt.xscale('log')
plt.yscale('log')
plt.savefig('DMvLum')
plt.close()
"""

"""
# testing and fixing Sawala
min_lums = 10**np.linspace(3,7,25)
halo_mass = 1.6*10**12
model = am.Sawala()
N_visible = np.array([model.ngreater(halo_mass,minlum)[0] for minlum in min_lums])
print N_visible
"""

