
from FeaturesAll import *

config = {
    "features": "SP500", 
}

f = featureBuilder(config)

desc = f.getDescription()
values = f.getFeature(datetime(2021,1,1), datetime(2022,1,1), timedelta(hours=1))
print(desc[0:20])
for i in range(100):
    print(np.mean(values[:,1+i*5]), np.mean(values[:,2+i*5]), np.mean(values[:,3+i*5]), np.mean(values[:,4+i*5]))
print(values.shape)