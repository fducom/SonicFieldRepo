/* For Copyright and License see LICENSE.txt and COPYING.txt in the root directory */
package com.nerdscentral.audio.combine;

import com.nerdscentral.audio.SFConstants;
import com.nerdscentral.audio.SFData;
import com.nerdscentral.audio.SFSignal;
import com.nerdscentral.sython.Caster;
import com.nerdscentral.sython.SFMaths;
import com.nerdscentral.sython.SFPL_Context;
import com.nerdscentral.sython.SFPL_Operator;
import com.nerdscentral.sython.SFPL_RuntimeException;

public class SF_Trim implements SFPL_Operator
{

    /**
     * 
     */
    private static final long serialVersionUID = 1L;

    @Override
    public Object Interpret(final Object input, final SFPL_Context context) throws SFPL_RuntimeException
    {
        try (SFSignal dataIn = Caster.makeSFSignal(input);)
        {
            int start = 0;
            int len = dataIn.getLength();
            for (; start < len; ++start)
            {
                if (SFMaths.abs(dataIn.getSample(start)) > SFConstants.NOISE_FLOOR) break;
            }
            int end = len - 1;
            for (; end > start; --end)
            {
                if (SFMaths.abs(dataIn.getSample(end)) > SFConstants.NOISE_FLOOR) break;
            }
            ++end;
            try (SFData out = SFData.build(end - start);)
            {
                for (int i = start; i < end; ++i)
                {
                    out.setSample(i - start, dataIn.getSample(i));
                }
                return Caster.prep4Ret(out);
            }
        }
    }

    @Override
    public String Word()
    {
        return Messages.getString("SF_Trim.0"); //$NON-NLS-1$
    }

}