/* For Copyright and License see LICENSE.txt and COPYING.txt in the root directory */
package com.nerdscentral.audio.pitch;

import java.util.List;

import com.nerdscentral.audio.core.SFSignal;
import com.nerdscentral.audio.pitch.algorithm.SFFilterGenerator;
import com.nerdscentral.audio.pitch.algorithm.SFFilterGenerator.NPoleFilterDef;
import com.nerdscentral.sython.Caster;
import com.nerdscentral.sython.SFPL_Operator;
import com.nerdscentral.sython.SFPL_RuntimeException;

public class SF_NHighPass extends SFNPoleFilterOperator implements SFPL_Operator
{

    private static final long serialVersionUID = 1L;

    @Override
    public String Word()
    {
        return Messages.getString("SFFilter_NHighPass.0");  //$NON-NLS-1$
    }

    @Override
    public Object Interpret(Object input) throws SFPL_RuntimeException
    {
        List<Object> l = Caster.makeBunch(input);
        try (SFSignal x = Caster.makeSFSignal(l.get(0)))
        {
            double frequency = Caster.makeDouble(l.get(1));
            double order = Caster.makeDouble(l.get(2));
            if (order > 11) throw new SFPL_RuntimeException(Messages.getString("SFFilter_NHighPass.1") + ((int) order)); //$NON-NLS-1$
            NPoleFilterDef fd = SFFilterGenerator.computeButterworthNHP(frequency, (int) order);
            try (SFSignal y = x.replicateEmpty())
            {
                filterLoop(x, y, fd, fd.getGainhf());
                return Caster.prep4Ret(y);
            }
        }
    }
}
