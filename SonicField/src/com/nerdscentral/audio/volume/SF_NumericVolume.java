/* For Copyright and License see LICENSE.txt and COPYING.txt in the root directory */
package com.nerdscentral.audio.volume;

import java.util.List;

import com.nerdscentral.audio.SFSignal;
import com.nerdscentral.audio.SFSingleTranslator;
import com.nerdscentral.sython.Caster;
import com.nerdscentral.sython.SFPL_Context;
import com.nerdscentral.sython.SFPL_Operator;
import com.nerdscentral.sython.SFPL_RuntimeException;

/**
 * ?s1,-3:Sf.Volume !s1_normal... forwards an SFData less 3 db ...
 * 
 * @author AlexTu
 * 
 */

public class SF_NumericVolume implements SFPL_Operator
{
    public static class Translator extends SFSingleTranslator
    {
        private final double volumeInner;

        Translator(SFSignal input, double volumeIn)
        {
            super(input);
            volumeInner = volumeIn;
        }

        @Override
        public double getSample(int index)
        {
            return getInputSample(index) * volumeInner;
        }

    }

    /**
     * 
     */
    private static final long serialVersionUID = 1L;

    @Override
    public Object Interpret(final Object input, final SFPL_Context context) throws SFPL_RuntimeException
    {
        List<Object> inList = Caster.makeBunch(input);
        try (SFSignal data = Caster.makeSFSignal(inList.get(0)).replicate();)
        {
            double scale = Caster.makeDouble(inList.get(1));
            try (SFSignal x = new Translator(data, scale))
            {
                return Caster.prep4Ret(x);
            }
        }
    }

    @Override
    public String Word()
    {
        return Messages.getString("SF_NumericVolume.0"); //$NON-NLS-1$
    }

}