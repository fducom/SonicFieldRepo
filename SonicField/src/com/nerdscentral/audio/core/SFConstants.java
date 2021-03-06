/* For Copyright and License see LICENSE.txt and COPYING.txt in the root directory */
package com.nerdscentral.audio.core;

import java.io.File;
import java.util.HashMap;
import java.util.concurrent.atomic.AtomicInteger;

import com.nerdscentral.audio.Messages;
import com.nerdscentral.sython.Caster;
import com.nerdscentral.sython.SFMaths;
import com.nerdscentral.sython.SFPL_RuntimeException;

@SuppressWarnings("nls")
public class SFConstants
{
    public static final double                   SPEED_OF_SOUND      = 340.29d;
    public static final double                   THREE_DBS           = 3.0102999566398119521373889472449d;
    public static double                         SAMPLE_RATE         = 96000.0;
    public static double                         SAMPLE_RATE_MS      = 96.0;
    public static final double                   TWELTH_ROOT_TWO     = Math.pow(2.0d, 1.0d / 12.0d);
    public static final double                   A4                  = 440;
    public static final double                   C4                  = 261.625565;
    public static final double                   LINEAR_CENT         = 0.0005946d;
    public static final double                   CENT                = SFMaths.pow(2.0d, 1.0d / 1200.0d);

    private final static HashMap<String, Double> equalNotes          = new HashMap<>();
    private final static HashMap<String, Double> justNotes           = new HashMap<>();
    public static final int                      defaultSplitAt      = (int) SAMPLE_RATE;
    private static double[]                      internalDBS         = new double[8001];
    public final static long                     ONE_MEG             = 1024 * 1024;
    public final static long                     ONE_GIG             = 1024 * 1024 * 1024;
    public static final double                   UPPER_AUDIBLE_LIMIT = 20000;
    public static final double                   UPPER_ALIAS_LIMIT   = 24000;
    public static final double                   NOISE_FLOOR         = 1.0 / 32768.00;
    public static final int                      PAGE_SIZE_DOUBLES   = 512;
    public static final boolean                  FIND_DEADLOCKS      = Boolean
                    .parseBoolean(System.getProperty("sython.check.deadlocks", "false"));
    public static final boolean                  CHECK_MEMORY        = Boolean
                    .parseBoolean(System.getProperty("sython.check.memory", "false"));

    public static boolean                        TRACE               = false;
    public static final String                   RESTART_DIRECTORY   = System.getProperty("sython.restart.dir",
                    System.getProperty("java.io.tmpdir"));
    public static final String                   CACHE_DIRECTORY     = System.getProperty("sython.cache.dir",
                    System.getProperty("java.io.tmpdir"));
    public static final String                   STORE_DIRECTORY     = System.getProperty("sython.store.dir",
                    System.getProperty("java.io.tmpdir"));
    public static final long                     HEART_BEAT          = Long
                    .valueOf(System.getProperty("sython.heart_beat", "240"));

    static
    {
        double start = C4 / 16; // C0
        // Add sharps and fundamentals
        for (int octave = 0; octave < 10; ++octave)
        {
            for (String rootName : new String[] { "c", "d", "e", "f", "g", "a", "b" })
            {
                equalNotes.put(rootName + octave, start);
                start *= TWELTH_ROOT_TWO;
                if (!(rootName.equals("b") || rootName.equals("e"))) //$NON-NLS-2$
                {
                    equalNotes.put(rootName + octave + "#", start); //$NON-NLS-1$
                    start *= TWELTH_ROOT_TWO;
                }
            }
        }
        start = C4 / 16; // C0
        // Add flats
        for (int octave = 0; octave < 10; ++octave)
        {
            for (String rootName : new String[] { "c", "d", "e", "f", "g", "a", "b" })
            {
                // if has a flat add it
                if (!(rootName.equals("c") || rootName.equals("f")))
                {
                    equalNotes.put(rootName + octave + "b", start / TWELTH_ROOT_TWO);
                }
                start *= TWELTH_ROOT_TWO;
                if (!(rootName.equals("b") || rootName.equals("e")))
                {
                    start *= TWELTH_ROOT_TWO;
                }
            }
        }
        for (double d = -400; d < 400.1; d += 0.1)
        {
            internalDBS[computeDBSOffset(d)] = slowFromDBs(d);
        }
        // Just notes
        start = C4 / 16; // C0
        for (int octave = 0; octave < 10; ++octave)
        {
            fillInJusts(octave, start);
            start *= 2;
        }
    }

    private static void fillInJusts(int rootName, double rootFrequency)
    {
        justNotes.put("c" + rootName, rootFrequency); //$NON-NLS-1$

        justNotes.put("c" + rootName + "#", rootFrequency * 16 / 15); //$NON-NLS-2$
        justNotes.put("d" + rootName + "b", rootFrequency * 16 / 15); //$NON-NLS-2$

        justNotes.put("d" + rootName, rootFrequency * 9 / 8); //$NON-NLS-1$

        justNotes.put("d" + rootName + "#", rootFrequency * 6 / 5); //$NON-NLS-2$
        justNotes.put("e" + rootName + "b", rootFrequency * 6 / 5); //$NON-NLS-2$

        justNotes.put("e" + rootName, rootFrequency * 5 / 4); //$NON-NLS-1$

        justNotes.put("f" + rootName, rootFrequency * 4 / 3); //$NON-NLS-1$

        justNotes.put("f" + rootName + "#", rootFrequency * 10 / 7); //$NON-NLS-2$
        justNotes.put("g" + rootName + "b", rootFrequency * 10 / 7); //$NON-NLS-2$

        justNotes.put("g" + rootName, rootFrequency * 3 / 2); //$NON-NLS-1$

        justNotes.put("g" + rootName + "#", rootFrequency * 32 / 21); //$NON-NLS-2$
        justNotes.put("a" + rootName + "b", rootFrequency * 32 / 21); //$NON-NLS-2$

        justNotes.put("a" + rootName, rootFrequency * 5 / 3); //$NON-NLS-1$

        justNotes.put("a" + rootName + "#", rootFrequency * 9 / 5); //$NON-NLS-2$
        justNotes.put("b" + rootName + "b", rootFrequency * 9 / 5); //$NON-NLS-2$

        justNotes.put("b" + rootName, rootFrequency * 15 / 8); //$NON-NLS-1$
    }

    public static final double getEqualPitch(String note) throws SFPL_RuntimeException
    {
        Object ret = equalNotes.get(note.toLowerCase());
        if (ret == null)
            throw new RuntimeException(Messages.getString("SFConstants.0") + note + Messages.getString("SFConstants.1")); //$NON-NLS-2$
        return Caster.makeDouble(ret);
    }

    /**
     * @param to
     */
    public static final double closesJustNote(double to)
    {
        double q = 0;
        double d = Double.MAX_VALUE;
        for (Double v : equalNotes.values())
        {

            double m = SFMaths.abs(v - q);
            if (m < d)
            {
                d = m;
                q = v;
            }
        }
        return q;
    }

    public static final double getJustPitch(String note) throws SFPL_RuntimeException
    {
        Object ret = justNotes.get(note.toLowerCase());
        if (ret == null)
            throw new RuntimeException(Messages.getString("SFConstants.0") + note + Messages.getString("SFConstants.1"));
        return Caster.makeDouble(ret);
    }

    public static double fromDBs(double dbs)
    {
        int x = computeDBSOffset(dbs);
        return x < 0 ? 0 : internalDBS[x];
    }

    private static int computeDBSOffset(double dbs)
    {
        return (int) ((dbs + 400) * 10);
    }

    public static double slowFromDBs(double dbs)
    {
        return SFMaths.pow(10, dbs / 20.0);
    }

    public static double slowToDBs(double dbs)
    {
        return Math.log10(dbs) * 20.0;
    }

    public static void setSampleRate(double rate)
    {
        SAMPLE_RATE = rate;
        SAMPLE_RATE_MS = rate / 1000.0d;
    }

    // Directory to send swap files to
    private static final String  SONIC_FIELD_TEMP = "sython.temp.dirs";
    public final static String[] TEMP_DATA_DIRS;
    static
    {
        String tempEnv = System.getProperty(SONIC_FIELD_TEMP);
        String[] tdNames = null;
        if (tempEnv == null)
        {
            tdNames = new String[] { System.getProperty("java.io.tmpdir") };
        }
        else
        {
            tdNames = tempEnv.split(","); //$NON-NLS-1$
        }
        TEMP_DATA_DIRS = tdNames;
    }

    private static class LocalisedTempDir extends ThreadLocal<File>
    {
        private final AtomicInteger tempRoundRobbin = new AtomicInteger();

        @Override
        protected File initialValue()
        {
            int frr = tempRoundRobbin.incrementAndGet() % TEMP_DATA_DIRS.length;
            return new File(TEMP_DATA_DIRS[frr]);
        }

        File getRoundRobbin()
        {
            return initialValue();
        }
    }

    @SuppressWarnings("synthetic-access")
    private static LocalisedTempDir LOCALISE_TEMPDIR = new LocalisedTempDir();

    public static File getLocalisedTempDir()
    {
        return LOCALISE_TEMPDIR.get();
    }

    public static File getRotatingTempDir()
    {
        return LOCALISE_TEMPDIR.getRoundRobbin();
    }

}
