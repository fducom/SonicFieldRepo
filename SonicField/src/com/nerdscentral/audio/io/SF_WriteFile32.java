/* For Copyright and License see LICENSE.txt and COPYING.txt in the root directory */
package com.nerdscentral.audio.io;

import java.util.List;

import com.nerdscentral.audio.Messages;
import com.nerdscentral.audio.sound.SF2JavaSound;
import com.nerdscentral.sython.Caster;
import com.nerdscentral.sython.SFPL_Operator;
import com.nerdscentral.sython.SFPL_RuntimeException;

/**
 * (?left,?right:),"temp.wav":Sf.WriteFile32 ... converts SFData channels to a 32 bit wav file a SFConstants.SAMPLE_RATE sps ...
 * 
 * @author AlexTu
 * 
 */
public class SF_WriteFile32 implements SFPL_Operator
{

    /**
     * 
     */
    private static final long serialVersionUID = 1L;

    @Override
    public Object Interpret(final Object input) throws SFPL_RuntimeException
    {
        List<Object> inList = Caster.makeBunch(input);
        List<Object> channels = Caster.makeBunch(inList.get(0));
        String fileName = (String) inList.get(1);
        try
        {
            SF2JavaSound.WriteWav(fileName, channels, true);
            return channels;
        }
        catch (Exception e)
        {
            throw new SFPL_RuntimeException(Messages.getString("cSFPL_SonicFieldLib.19"), e); //$NON-NLS-1$
        }
    }

    @Override
    public String Word()
    {
        return Messages.getString("cSFPL_SonicFieldLib.20"); //$NON-NLS-1$
    }

}