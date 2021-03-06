/* For Copyright and License see LICENSE.txt and COPYING.txt in the root directory */
package com.nerdscentral.audio.generators;

import java.util.List;

import com.nerdscentral.audio.core.SFConstants;
import com.nerdscentral.audio.core.SFData;
import com.nerdscentral.audio.core.SFSignal;
import com.nerdscentral.sython.Caster;
import com.nerdscentral.sython.SFMaths;
import com.nerdscentral.sython.SFPL_Operator;
import com.nerdscentral.sython.SFPL_RuntimeException;

public class SF_PhaseModulatedSin implements SFPL_Operator
{
    private static final long serialVersionUID = 1L;

    @Override
    public String Word()
    {
        return Messages.getString("SF_PhaseModulatedSin.0"); //$NON-NLS-1$
    }

    @Override
    public Object Interpret(Object input) throws SFPL_RuntimeException
    {
        final List<Object> l = Caster.makeBunch(input);
        final double frequency = Caster.makeDouble(l.get(0));
        final SFSignal phase = (Caster.makeSFSignal(l.get(1)));
        int size = phase.getLength();
        SFSignal data = SFData.build(size, false);
        final double PI2 = SFMaths.PI * 2.0d;
        // Use the periodic nature of a sin wave to save cpu
        for (int i = 0; i < size; ++i)
        {
            data.setSample(i, SFMaths.sin((i * PI2 * frequency / SFConstants.SAMPLE_RATE) + (PI2 * phase.getSample(i))));
        }
        return data;
    }
}