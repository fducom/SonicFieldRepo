/* For Copyright and License see LICENSE.txt and COPYING.txt in the root directory */
package com.nerdscentral.data;

import java.util.MissingResourceException;
import java.util.ResourceBundle;

public class Messages
{
    private static final String         BUNDLE_NAME     = "com.nerdscentral.data.messages";     //$NON-NLS-1$

    private static final ResourceBundle RESOURCE_BUNDLE = ResourceBundle.getBundle(BUNDLE_NAME);

    private Messages()
    {
    }

    public static String getString(String key)
    {
        try
        {
            return RESOURCE_BUNDLE.getString(key);
        }
        catch (MissingResourceException e)
        {
            return '!' + key + '!';
        }
    }
}
