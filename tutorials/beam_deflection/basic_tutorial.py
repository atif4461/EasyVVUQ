import os
import easyvvuq as uq
import chaospy as cp
import matplotlib.pyplot as plt

from easyvvuq.actions import QCGPJPool
from easyvvuq.actions import CreateRunDirectory, Encode, Decode, ExecuteLocal, Actions

params = {
    "F": {"type": "float", "default": 1.0},
    "L": {"type": "float", "default": 1.5},
    "a": {"type": "float", "min": 0.7, "max": 1.2, "default": 1.0},
    "D": {"type": "float", "min": 0.75, "max": 0.85, "default": 0.8},
    "d": {"type": "float", "default": 0.1},
    "E": {"type": "float", "default": 200000},
    "outfile": {"type": "string", "default": "beam_output.json"}
}



encoder = uq.encoders.GenericEncoder(template_fname='beam.template', delimiter='$', target_filename='beam_input.json')
decoder = uq.decoders.JSONDecoder(target_filename='beam_output.json', output_columns=['g1'])
execute = ExecuteLocal('{}/beam beam_input.json'.format(os.getcwd()))

actions = Actions(CreateRunDirectory('/tmp'),
                  Encode(encoder), execute, Decode(decoder))

campaign = uq.Campaign(name='beam', params=params, actions=actions)
#campaign = uq.Campaign(name='beam', params=params, encoder=encoder, decoder=decoder)

vary = {
    "F": cp.Normal(1, 0.1),
    "L": cp.Normal(1.5, 0.01),
    "a": cp.Uniform(0.7, 1.2),
    "D": cp.Triangle(0.75, 0.8, 0.85)
}

campaign.set_sampler(uq.sampling.PCESampler(vary=vary, polynomial_order=1))

campaign.execute().collate()
campaign.get_collation_result()

results = campaign.analyse(qoi_cols=['g1'])

#results.plot_sobols_treemap('g1', figsize=(10, 10))
#plt.axis('off');

print("sobols_first('g1)          :", results.sobols_first('g1'))
print("supported stats            :", results.supported_stats())
print("get_sobols_first('g1', 'F'):", results._get_sobols_first('g1', 'F'))
print("sobols_total('g1', 'F')    :", results.sobols_total('g1', 'F'))

print("success")

