/* For Copyright and License see LICENSE.txt and COPYING.txt in the root directory */
package com.nerdscentral.audio.sound;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.SourceDataLine;

import com.nerdscentral.audio.Messages;
import com.nerdscentral.audio.core.SFConstants;
import com.nerdscentral.audio.core.SFPL_RefPassThrough;
import com.nerdscentral.audio.core.SFSignal;
import com.nerdscentral.audio.volume.SF_Normalise;
import com.nerdscentral.sython.Caster;
import com.nerdscentral.sython.SFPL_Operator;
import com.nerdscentral.sython.SFPL_RuntimeException;

public class SF_Monitor implements SFPL_Operator, SFPL_RefPassThrough
{

    private static final long serialVersionUID = 1L;

    @Override
    public String Word()
    {
        return Messages.getString("SF_Monitor.0"); //$NON-NLS-1$
    }

    @Override
    public Object Interpret(Object input) throws SFPL_RuntimeException
    {
        SFSignal data = Caster.makeSFSignal(input);
        SFSignal dataIn = SF_Normalise.doNormalisation(data);
        try
        {
            AudioFormat af = new AudioFormat((float) SFConstants.SAMPLE_RATE, 16, 1, true, true);
            DataLine.Info info = new DataLine.Info(SourceDataLine.class, af);
            SourceDataLine source = (SourceDataLine) AudioSystem.getLine(info);
            source.open(af);
            source.start();
            byte[] buf = new byte[dataIn.getLength() * 2];
            for (int i = 0; i < buf.length; ++i)
            {
                short sample = (short) (dataIn.getSample(i / 2) * 32767.0);
                buf[i] = (byte) (sample >> 8);
                buf[++i] = (byte) (sample & 0xFF);
            }
            source.write(buf, 0, buf.length);
            source.drain();
            source.stop();
            source.close();
            return data;
        }
        catch (Exception e)
        {
            throw new SFPL_RuntimeException(Messages.getString("SF_Monitor.1"), e); //$NON-NLS-1$
        }
    }
}
